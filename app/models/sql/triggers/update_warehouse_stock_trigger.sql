-- Функция для обновления остатков на складе при движении товаров
CREATE OR REPLACE FUNCTION public.update_warehouse_stock()
RETURNS TRIGGER AS $$
BEGIN
    -- Для прихода товара
    IF NEW.event_type = 'arrival' THEN
        INSERT INTO stocks (warehouse_id, product_id, quantity)
        VALUES (NEW.warehouse_id, NEW.product_id, NEW.quantity)
        ON CONFLICT (warehouse_id, product_id) 
        DO UPDATE SET 
            quantity = stocks.quantity + EXCLUDED.quantity;
    
    -- Для расхода товара
    ELSIF NEW.event_type = 'departure' THEN
        -- Проверяем, достаточно ли товара на складе
        IF NOT EXISTS (
            SELECT 1 FROM stocks 
            WHERE warehouse_id = NEW.warehouse_id 
            AND product_id = NEW.product_id
            AND quantity >= NEW.quantity
        ) THEN
            RAISE EXCEPTION 'Недостаточно товара % на складе %', 
                (SELECT name FROM products WHERE id = NEW.product_id),
                (SELECT source FROM warehouses WHERE id = NEW.warehouse_id);
        END IF;
        
        -- Обновляем остаток
        UPDATE stocks
        SET quantity = quantity - NEW.quantity
        WHERE warehouse_id = NEW.warehouse_id 
        AND product_id = NEW.product_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создаем триггер, который вызывает нашу функцию
CREATE OR REPLACE TRIGGER movement_after_insert
AFTER INSERT ON movements
FOR EACH ROW
EXECUTE FUNCTION public.update_warehouse_stock();

-- Комментарии для документации
COMMENT ON FUNCTION public.update_warehouse_stock() IS 
'Обновляет остатки на складе при добавлении движения товара.
При приходе - увеличивает количество, при расходе - уменьшает.
При недостатке товара на складе вызывает исключение.';
