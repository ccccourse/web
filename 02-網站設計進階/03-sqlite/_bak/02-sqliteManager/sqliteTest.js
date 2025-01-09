import { DB } from "https://deno.land/x/sqlite/mod.ts";

try {
  Deno.remove("mydb.db")
} catch (e) {
  console.log('remove fail!')
}
const db = new DB("mydb.db");
db.query("CREATE TABLE users (user TEXT, pass TEXT)");
db.query("CREATE TABLE msgs (msg TEXT, user TEXT)");

const users = [
  ["ccc", "123"],
  ["tim", "321"]
];

for (const [user,pass] of users)
  db.query("INSERT INTO users (user, pass) VALUES (?,?)", 
           [user, pass]);

for (const [user,pass] of db.query("SELECT user,pass FROM users"))
  console.log(user, pass);

let r = db.query(`SELECT name FROM sqlite_schema
  WHERE type ='table' AND name NOT LIKE 'sqlite_%'`)
console.log('r=', r)
db.close()
