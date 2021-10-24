var mysql = require('mysql');
var conn = mysql.createConnection({
  host: 'localhost', // Replace with your host name
  user: 'pi',      // Replace with your database username
  password: 'password',      // Replace with your database password
  database: 'callid' // // Replace with your database Name
}); 
conn.connect(function(err) {
  if (err) throw err;
  console.log('Database is connected successfully !');
});
module.exports = conn;
