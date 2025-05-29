/*
This view is for SJTU Global
We want to filter out pages cared by the group "sjtu_global"
I wanted logic:
- select group_id of "sjtu_global"
- select pages, with condition
- group has many categories
- categories have many sites
- only show pages that in these sites
*/
CREATE VIEW page4global AS
SELECT
    page.id AS id,
    page.title AS title_raw,
    page.title_cn AS title_cn,
    page.full_content AS content_raw,
    page.full_content_cn AS content_cn,
    page.content AS summary_cn,
    page.publish_time AS publish_date,
    page.score AS score,
    site.name AS school_name,
    page.source_url AS source_url
FROM
    page
    JOIN site ON page.site_id = site.id
    JOIN category_site_relation ON site.id = category_site_relation.site_id
    JOIN category ON category.id = category_site_relation.category_id
    JOIN "group" g ON category.group_id = g.id
WHERE
    g.id = TO_FILL;
-- Replace TO_FILL with the actual group_id of "sjtu_global"