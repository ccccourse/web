import { DB } from "https://deno.land/x/sqlite/mod.ts";

try {
  Deno.remove("mydb.db")
} catch (e) {
  console.log('remove fail!')
}
const db = new DB("mydb.db");
while (true) {
  let command = prompt('sql?')
  if (command=='exit') break
  if (command == '.tables')
    command = "SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%'"
  try {
    let r = db.query(command)
    console.log(r)
  } catch (error) {
    console.log('error=', error)
  }
}

db.close();
