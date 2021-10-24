var express = require('express');
var router = express.Router();
var db=require('../database');

router.get('/', function(req, res, next) {
  var sql='select * from call_log where time_stamp BETWEEN NOW() - INTERVAL 14 DAY and NOW();';
  db.query(sql, function (err, data, fields) {
    if (err) throw err;
    res.render('index', { title: 'Call Firewall: Statistics', callData: data });
  });
});

module.exports = router;
