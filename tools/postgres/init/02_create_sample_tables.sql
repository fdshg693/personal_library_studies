-- サンプルテーブルの作成スクリプト

-- ユーザーテーブル
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- インデックス作成
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

-- 更新日時自動更新用トリガー関数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- トリガー設定
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- サンプルデータ挿入
INSERT INTO users (username, email, password_hash) VALUES
    ('admin', 'admin@example.com', crypt('password123', gen_salt('bf'))),
    ('user1', 'user1@example.com', crypt('password123', gen_salt('bf'))),
    ('user2', 'user2@example.com', crypt('password123', gen_salt('bf'))),
    ('john_doe', 'john.doe@example.com', crypt('password123', gen_salt('bf'))),
    ('jane_smith', 'jane.smith@example.com', crypt('password123', gen_salt('bf'))),
    ('mike_johnson', 'mike.j@example.com', crypt('password123', gen_salt('bf'))),
    ('sarah_williams', 'sarah.w@example.com', crypt('password123', gen_salt('bf'))),
    ('david_brown', 'david.brown@example.com', crypt('password123', gen_salt('bf'))),
    ('emily_davis', 'emily.davis@example.com', crypt('password123', gen_salt('bf'))),
    ('alex_garcia', 'alex.garcia@example.com', crypt('password123', gen_salt('bf'))),
    ('maria_rodriguez', 'maria.r@example.com', crypt('password123', gen_salt('bf'))),
    ('robert_wilson', 'robert.wilson@example.com', crypt('password123', gen_salt('bf'))),
    ('lisa_anderson', 'lisa.anderson@example.com', crypt('password123', gen_salt('bf'))),
    ('kevin_thomas', 'kevin.t@example.com', crypt('password123', gen_salt('bf'))),
    ('amanda_taylor', 'amanda.taylor@example.com', crypt('password123', gen_salt('bf'))),
    ('chris_lee', 'chris.lee@example.com', crypt('password123', gen_salt('bf'))),
    ('jessica_white', 'jessica.white@example.com', crypt('password123', gen_salt('bf'))),
    ('daniel_harris', 'daniel.h@example.com', crypt('password123', gen_salt('bf'))),
    ('megan_clark', 'megan.clark@example.com', crypt('password123', gen_salt('bf'))),
    ('ryan_lewis', 'ryan.lewis@example.com', crypt('password123', gen_salt('bf'))),
    ('nicole_walker', 'nicole.w@example.com', crypt('password123', gen_salt('bf'))),
    ('brandon_hall', 'brandon.hall@example.com', crypt('password123', gen_salt('bf'))),
    ('stephanie_allen', 'stephanie.a@example.com', crypt('password123', gen_salt('bf'))),
    ('jason_young', 'jason.young@example.com', crypt('password123', gen_salt('bf'))),
    ('michelle_king', 'michelle.king@example.com', crypt('password123', gen_salt('bf'))),
    ('andrew_wright', 'andrew.wright@example.com', crypt('password123', gen_salt('bf'))),
    ('laura_lopez', 'laura.lopez@example.com', crypt('password123', gen_salt('bf'))),
    ('justin_hill', 'justin.h@example.com', crypt('password123', gen_salt('bf'))),
    ('rachel_green', 'rachel.green@example.com', crypt('password123', gen_salt('bf'))),
    ('matthew_adams', 'matthew.adams@example.com', crypt('password123', gen_salt('bf'))),
    ('olivia_baker', 'olivia.baker@example.com', crypt('password123', gen_salt('bf'))),
    ('tyler_gonzalez', 'tyler.g@example.com', crypt('password123', gen_salt('bf'))),
    ('hannah_nelson', 'hannah.nelson@example.com', crypt('password123', gen_salt('bf'))),
    ('joshua_carter', 'joshua.carter@example.com', crypt('password123', gen_salt('bf'))),
    ('samantha_mitchell', 'samantha.m@example.com', crypt('password123', gen_salt('bf'))),
    ('nathan_perez', 'nathan.perez@example.com', crypt('password123', gen_salt('bf'))),
    ('victoria_roberts', 'victoria.r@example.com', crypt('password123', gen_salt('bf'))),
    ('jacob_turner', 'jacob.turner@example.com', crypt('password123', gen_salt('bf'))),
    ('emma_phillips', 'emma.phillips@example.com', crypt('password123', gen_salt('bf'))),
    ('ethan_campbell', 'ethan.c@example.com', crypt('password123', gen_salt('bf'))),
    ('sophia_parker', 'sophia.parker@example.com', crypt('password123', gen_salt('bf'))),
    ('william_evans', 'william.evans@example.com', crypt('password123', gen_salt('bf'))),
    ('ava_edwards', 'ava.edwards@example.com', crypt('password123', gen_salt('bf'))),
    ('james_collins', 'james.collins@example.com', crypt('password123', gen_salt('bf'))),
    ('isabella_stewart', 'isabella.s@example.com', crypt('password123', gen_salt('bf'))),
    ('alexander_sanchez', 'alex.sanchez@example.com', crypt('password123', gen_salt('bf'))),
    ('mia_morris', 'mia.morris@example.com', crypt('password123', gen_salt('bf'))),
    ('liam_rogers', 'liam.rogers@example.com', crypt('password123', gen_salt('bf'))),
    ('charlotte_reed', 'charlotte.reed@example.com', crypt('password123', gen_salt('bf'))),
    ('noah_cook', 'noah.cook@example.com', crypt('password123', gen_salt('bf'))),
    ('amelia_morgan', 'amelia.morgan@example.com', crypt('password123', gen_salt('bf')))
ON CONFLICT DO NOTHING;

-- パフォーマンステスト用テーブル
CREATE TABLE IF NOT EXISTS performance_test (
    id SERIAL PRIMARY KEY,
    data TEXT,
    number INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- パフォーマンステスト用インデックス
CREATE INDEX IF NOT EXISTS idx_performance_number ON performance_test(number);
CREATE INDEX IF NOT EXISTS idx_performance_created_at ON performance_test(created_at);

-- 初期化完了メッセージ
DO $$
BEGIN
    RAISE NOTICE 'Sample tables created successfully!';
END $$;
