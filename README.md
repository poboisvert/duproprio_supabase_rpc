# realtor.ca_supabase
realtorca to supabase for analytics


Supabase update or insert (w/JSON)

I was having trouble to find documentation on how to save a JSON with RPC function of Supabase

```
CREATE OR REPLACE FUNCTION update_listing(page_slug TEXT, address TEXT, data jsonb)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
IF EXISTS (SELECT FROM listing1 WHERE slug=page_slug and is_active is True) THEN
UPDATE listing1
SET is_active = True,
updated_at = NOW()
WHERE slug = page_slug;
ELSE
INSERT into listing1(slug, address, data) VALUES (page_slug, address, data::JSON);
END IF;
END;
$$;
```````
