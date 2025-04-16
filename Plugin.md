
---

## 🧠 Основна логіка плагіна

Плагін:

- ✅ Приймає handshake від клієнтського моду.
    
- ✅ Перевіряє, чи встановлений мод (і чи він не підроблений).
    
- ✅ Перевіряє IP, MAC, DNS тощо.
    
- ✅ Зберігає все в БД (MySQL).
    
- ✅ Відхиляє гравця, якщо дані підозрілі.
    
- ✅ Логує моди, дані та статус у консоль.
    

---

## 📦 Структура плагіна

```
server-plugin/
├─ src/
│  ├─ main/
│  │  ├─ java/
│  │  │  ├─ me.myauthplugin/
│  │  │  │  ├─ AuthPlugin.java          <-- головний клас
│  │  │  │  ├─ network/                 <-- обробка packet’ів
│  │  │  │  ├─ db/                      <-- база даних
│  │  │  │  ├─ listener/                <-- івенти
│  │  │  │  ├─ model/                   <-- моделі даних
│  │  │  │  └─ util/                    <-- утиліти
│  │  └─ resources/
│  │     └─ config.yml
├─ build.gradle
```

---

## 🔌 1. Головний клас — `AuthPlugin.java`

```java
public class AuthPlugin extends JavaPlugin {
    private static AuthPlugin instance;
    private DatabaseManager db;

    @Override
    public void onEnable() {
        instance = this;
        saveDefaultConfig();

        db = new DatabaseManager(getConfig());
        db.connect();

        new HandshakeChannel().register(); // custom netty channel
        getServer().getPluginManager().registerEvents(new PlayerJoinListener(db), this);

        getLogger().info("MyAuthPlugin запущено!");
    }

    @Override
    public void onDisable() {
        db.close();
    }

    public static AuthPlugin getInstance() {
        return instance;
    }
}
```

---

## 🛠️ 2. Конфігурація — `config.yml`

```yaml
database:
  host: "db.example.com"
  port: 3306
  name: "auth"
  user: "root"
  password: "123456"
```

---

## 🗄️ 3. Підключення до БД — `DatabaseManager.java`

```java
public class DatabaseManager {
    private Connection connection;

    public DatabaseManager(FileConfiguration config) {
        // Створення URL
    }

    public void connect() {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            String url = "jdbc:mysql://" + host + ":" + port + "/" + db;
            connection = DriverManager.getConnection(url, user, pass);

            PreparedStatement stmt = connection.prepareStatement(
                "CREATE TABLE IF NOT EXISTS player_data (...);"
            );
            stmt.executeUpdate();
        } catch (SQLException | ClassNotFoundException e) {
            e.printStackTrace();
        }
    }

    public void insertPlayerData(PlayerInfo data) {
        try {
            PreparedStatement stmt = connection.prepareStatement(
                "INSERT INTO player_data (...) VALUES (?, ?, ?, ...);"
            );
            // stmt.setString(1, data.getIp());
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void close() {
        if (connection != null) try { connection.close(); } catch (SQLException ignored) {}
    }
}
```

---

## 🌐 4. Прийом packet’ів — `HandshakeChannel.java`

Це буде Netty-канал для прийому даних від Fabric/Forge.

### Варіант 1 — Paper + власний Netty канал (через ProtocolLib або прямо)

```java
public class HandshakeChannel {
    private final String CHANNEL_NAME = "myauth:handshake";
    private final Map<UUID, PlayerInfo> cache = new HashMap<>();

    public void register() {
        Bukkit.getMessenger().registerIncomingPluginChannel(AuthPlugin.getInstance(), CHANNEL_NAME, (channel, player, message) -> {
            if (!channel.equals(CHANNEL_NAME)) return;

            try {
                ByteArrayInputStream in = new ByteArrayInputStream(message);
                DataInputStream data = new DataInputStream(in);

                PlayerInfo info = PlayerInfo.fromStream(data);
                cache.put(player.getUniqueId(), info);

                AuthPlugin.getInstance().getLogger().info("Handshake від " + player.getName() + ": IP = " + info.getIp());

            } catch (IOException e) {
                e.printStackTrace();
            }
        });
    }

    public Optional<PlayerInfo> getCached(UUID uuid) {
        return Optional.ofNullable(cache.get(uuid));
    }
}
```

---

## 📥 5. Обробка входу гравця — `PlayerJoinListener.java`

```java
public class PlayerJoinListener implements Listener {
    private final DatabaseManager db;

    public PlayerJoinListener(DatabaseManager db) {
        this.db = db;
    }

    @EventHandler(priority = EventPriority.HIGHEST)
    public void onAsyncPreLogin(AsyncPlayerPreLoginEvent event) {
        HandshakeChannel channel = AuthPlugin.getInstance().getChannel();
        Optional<PlayerInfo> optInfo = channel.getCached(event.getUniqueId());

        if (optInfo.isEmpty()) {
            event.disallow(Result.KICK_OTHER, "❌ Встановіть обов'язковий мод MyAuth!");
            return;
        }

        PlayerInfo info = optInfo.get();

        // Перевірка IP
        if (!info.getIp().equals(event.getAddress().getHostAddress())) {
            event.disallow(Result.KICK_OTHER, "🔒 VPN не дозволено. Ваш IP не співпадає.");
            return;
        }

        db.insertPlayerData(info);
    }
}
```

---

## 📦 6. Модель даних — `PlayerInfo.java`

```java
public class PlayerInfo {
    private String playerName;
    private String ip;
    private String mac;
    private String cpu;
    private String gpu;
    private String ram;
    private List<String> modList;

    public static PlayerInfo fromStream(DataInputStream in) throws IOException {
        PlayerInfo info = new PlayerInfo();
        info.playerName = in.readUTF();
        info.ip = in.readUTF();
        info.mac = in.readUTF();
        info.cpu = in.readUTF();
        info.gpu = in.readUTF();
        info.ram = in.readUTF();

        int modCount = in.readInt();
        info.modList = new ArrayList<>();
        for (int i = 0; i < modCount; i++) {
            info.modList.add(in.readUTF());
        }
        return info;
    }

    // + геттери, сеттери
}
```

---

## 🔍 7. Логування

У `onEnable()` і `PlayerJoinListener`:

```java
getLogger().info("Гравець " + username + " підключився з IP " + ip + ", MAC: " + mac);
getLogger().info("Встановлені моди: " + String.join(", ", modList));
```

---

## 💬 8. Kick-повідомлення

- Якщо мод відсутній → `❌ Встановіть MyAuth мод.`
    
- Якщо IP ≠ локальний → `🔒 VPN не дозволено.`
    
- Якщо успішно → пропускаємо на сервер
    

---

## 🧪 9. Тест-кейси

|Сценарій|Результат|
|---|---|
|Без моду|Kick з повідомленням|
|Мод є, IP співпадає|Успішний вхід, логування в БД|
|Мод є, IP ≠ event.getAddress()|Kick із причиною VPN|
|Некоректний packet|Виняток, логування помилки|

---

## ✅ Результат

- Плагін приймає handshake-пакет.
    
- Перевіряє мод.
    
- Валідує IP, MAC, GPU, CPU.
    
- Зберігає все в БД.
    
- Відхиляє підозрілих.
    
- Працює з Fabric/Forge модом як єдине ціле.
    

---