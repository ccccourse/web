async function sqlRun() {
  let command = document.getElementById('command').value
  let rzjson = document.getElementById('resultJson')
  let r = await window.fetch(`/sqlcmd/${command}`)
  let obj = await r.json()
  rzjson.innerText = JSON.stringify(obj, null, 2)
}