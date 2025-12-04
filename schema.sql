-- 1. 启用插件
CREATE EXTENSION IF NOT EXISTS postgis;

-- 2. 核心表: memories
CREATE TABLE memories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id TEXT, -- 用户标识
  
  -- 地理信息 (核心)
  location GEOGRAPHY(POINT) NOT NULL, -- 真实坐标
  poi_name TEXT,     -- 高德返回: "浙大艺术考古博物馆"
  poi_address TEXT,  -- 高德返回: "西湖区余杭塘路866号"
  adcode TEXT,       -- 高德返回: 行政区划代码
  
  -- 内容信息
  image_url TEXT NOT NULL,
  content TEXT,      -- AI 生成的文案
  tags TEXT[],       -- AI 提取的标签 ['看展', '文物', '周末']
  mood TEXT,         -- 情绪
  
  -- 推荐权重
  quality_score FLOAT DEFAULT 0, 
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. 索引
CREATE INDEX idx_memories_geo ON memories USING GIST (location);
CREATE INDEX idx_memories_poi ON memories (poi_name);

-- 4. 创建获取附近记忆的函数
CREATE OR REPLACE FUNCTION get_nearby_memories(lat NUMERIC, lon NUMERIC, radius_meters INTEGER)
RETURNS TABLE(
    id UUID,
    user_id TEXT,
    poi_name TEXT,
    poi_address TEXT,
    adcode TEXT,
    image_url TEXT,
    content TEXT,
    tags TEXT[],
    mood TEXT,
    quality_score FLOAT,
    created_at TIMESTAMPTZ,
    distance_meters FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.id,
        m.user_id,
        m.poi_name,
        m.poi_address,
        m.adcode,
        m.image_url,
        m.content,
        m.tags,
        m.mood,
        m.quality_score,
        m.created_at,
        ST_Distance(m.location, ST_Point(lon, lat)::GEOGRAPHY) AS distance_meters
    FROM memories m
    WHERE ST_DWithin(m.location, ST_Point(lon, lat)::GEOGRAPHY, radius_meters)
    ORDER BY m.created_at DESC;
END;
$$ LANGUAGE plpgsql;