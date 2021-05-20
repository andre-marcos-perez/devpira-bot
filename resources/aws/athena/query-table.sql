-- Quantidade de mensagens por dia

SELECT "date", count(1) AS "message_amount" FROM "default"."devpira_enriched" GROUP BY "date" ORDER BY "date" DESC;

-- Quantidade de mensagens por usuário por dia

SELECT user_id, user_username, "date", count(1) AS "message_amount" FROM "default"."devpira_enriched" GROUP BY user_id, user_username, "date" ORDER BY "date" DESC;

-- Média do tamanho das mensagens por usuário por dia

SELECT user_id, user_username, "date", CAST(AVG(length(text)) AS INT) AS "average_message_length" FROM "default"."devpira_enriched" GROUP BY user_id, user_username, "date" ORDER BY "date" DESC;