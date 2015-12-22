#jdbc.url=jdbc:mysql://localhost:3306/ec?useUnicode=true&characterEncoding=utf-8

#postgreSql database setting
#jdbc.driver=org.postgresql.Driver
#jdbc.url=jdbc:postgresql://20.12.6.2:5432/model_design
#jdbc.username=pg
#jdbc.password=1


jdbc.driver=com.mysql.jdbc.Driver
jdbc.url=jdbc:mysql://172.20.8.115:3306/uspider_manager?useUnicode=true&characterEncoding=utf-8&autoReconnect=true&zeroDateTimeBehavior=convertToNull
jdbc.username=root
jdbc.password=udh*123



#connection pool settings
jdbc.pool.maxIdle=10
jdbc.pool.maxActive=50
jdbc.pool.maxWait=120000

#mail
mail.host=smtp.exmail.qq.com
mail.username=info@uradar.com.cn
mail.password=yonyou@123
mail.port=465