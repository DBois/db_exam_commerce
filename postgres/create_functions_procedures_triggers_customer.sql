DROP PROCEDURE IF EXISTS insert_creditcard;

CREATE OR REPLACE PROCEDURE insert_creditcard(p_card_number varchar, p_expiration_date varchar, p_customer_fk int) LANGUAGE plpgsql AS $$
	BEGIN 
		IF p_card_number ~ '^[0-9\.]+$' AND p_expiration_date ~ '^[0-9\.]+$' THEN 
			INSERT INTO credit_card(card_number, expiration_date, customer_fk) VALUES (p_card_number, p_expiration_date, p_customer_fk);
		END IF;
	END
$$;