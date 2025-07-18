-- Функция для обновления остатков на складе при движении товаров
CREATE OR REPLACE FUNCTION public.update_stock()
    RETURNS TRIGGER AS
$$
BEGIN
    -- Для прихода товара
    IF NEW.event_type = 'ARRIVAL'::movement_type THEN
        -- Добавляем товар на склад
        INSERT INTO stocks (warehouse_id, product_id, quantity)
        VALUES (NEW.warehouse_id, NEW.product_id, NEW.quantity)
        ON CONFLICT (warehouse_id, product_id)
            DO UPDATE SET quantity = stocks.quantity + EXCLUDED.quantity;

    -- Для расхода товара
    ELSIF NEW.event_type = 'DEPARTURE'::movement_type THEN
        -- Проверяем, достаточно ли товара на складе
        DECLARE
            current_quantity INTEGER;
        BEGIN
            SELECT COALESCE(quantity, 0) INTO current_quantity
            FROM stocks
            WHERE warehouse_id = NEW.warehouse_id
              AND product_id = NEW.product_id
            FOR UPDATE;  -- Блокируем строку для предотвращения гонок

            IF current_quantity < NEW.quantity THEN
                RAISE EXCEPTION 'Недостаточно товара % на складе %. Доступно: %, требуется: %',
                    (SELECT name FROM products WHERE id = NEW.product_id),
                    (SELECT source FROM warehouses WHERE id = NEW.warehouse_id),
                    current_quantity,
                    NEW.quantity;
            END IF;
        END;

        -- Списываем товар со склада
        UPDATE stocks
        SET quantity = quantity - NEW.quantity
        WHERE warehouse_id = NEW.warehouse_id
          AND product_id = NEW.product_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Удаляем старый триггер, если существует
DROP TRIGGER IF EXISTS movement_after_insert ON movements;

-- Создаем триггер, который вызывает нашу функцию
CREATE TRIGGER movement_after_insert
    AFTER INSERT
    ON movements
    FOR EACH ROW
EXECUTE FUNCTION public.update_stock();

-- Комментарии для документации
COMMENT ON FUNCTION public.update_stock() IS
    'Обновляет остатки на складе при добавлении движения товара.
    При приходе - увеличивает количество, при расходе - уменьшает.
    При недостатке товара на складе вызывает исключение с информацией о доступном количестве.';
