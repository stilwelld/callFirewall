var express = require('express');
var router = express.Router();
var db=require('../database');
var bodyParser = require('body-parser');

var jsonParser = bodyParser.json();

router.get('/', function(req, res, next) {
  var sql='SELECT * from call_log ORDER BY id DESC';
  db.query(sql, function (err, data, fields) {
    if (err) throw err;
    res.render('callid', { title: 'Call Log', callData: data });
  });
});

// BLOCK 

router.get('/block', function(req, res, next) {
  var sql='SELECT * from block';
  db.query(sql, function (err, data, fields) {
    if (err) throw err;
    res.render('block', { title: 'Blocked information', blockData: data });
  });
});

router.get('/block/insert/:nmbr', function(req, res, next) {
  const nmbr = req.params;

  var sql='SELECT * from block where NMBR= ?';
  db.query(sql, req.params.nmbr, function (err, row) {
    if (err) { 
       throw err; 
    } else {
       if (row && row.length) {
	  console.log("Nmbr already exists")
       } else {
          var sql='INSERT INTO block SET ?';
          db.query(sql, nmbr, function (err, data) {
             if (err) throw err;
          });
       }
    }
  });
  res.redirect('/callid/block'); // redirect to the block table
});
module.exports = router;

router.post('/block/insert/', function(req, res, next) {
  console.log(req.body);
  var nmbr = req.body.nmbr;
  console.log("Nmbr ="+nmbr)
  var name = req.body.name;
  console.log("Name ="+name)
  var sql='INSERT INTO block SET ?';
  db.query(sql, req.body, function (err, data) {
     if (err) throw err;
  });
  res.redirect('/callid/block'); // redirect to the block table
});

router.get('/block/delete/:id', function(req, res, next) {
  const id = req.params;
  var sql='DELETE FROM block WHERE ID= ?';
  db.query(sql, req.params.id, function (err, data) {
    if (err) throw err;
  });
  res.redirect('/callid/block'); // redirect to the block table
});
module.exports = router;

router.get('/block', function(req, res, next) {
  var sql='SELECT * from block';
  db.query(sql, function (err, data, fields) {
    if (err) throw err;
    res.render('block', { title: 'Blocked information', blockData: data });
  });
});

// ALLOW

router.get('/allow', function(req, res, next) {
  var sql='SELECT * from allow';
  db.query(sql, function (err, data, fields) {
    if (err) throw err;
    res.render('allow', { title: 'Allowed information', blockData: data });
  });
});

router.post('/allow/insert/', function(req, res, next) {
  console.log(req.body);
  var id = req.body.id;
  var nmbr = req.body.nmbr;
  console.log("Nmbr ="+nmbr)
  var name = req.body.name;
  console.log("Name ="+name)
  if (id) {
    var sql='UPDATE allow SET nmbr="'+nmbr+'", name="'+name+'" WHERE ID="'+id+'";';
    db.query(sql, req.body, function (err, data) {
     if (err) throw err;
    });
  } else {
    var sql='INSERT INTO allow SET ?';
    db.query(sql, req.body, function (err, data) {
       if (err) throw err;
    });
  }
  res.redirect('/callid/allow'); // redirect to the block table
});

router.get('/allow/insert/:nmbr', function(req, res, next) {
  const nmbr = req.params;

  var sql='SELECT * from allow where NMBR= ?';
  db.query(sql, req.params.nmbr, function (err, row) {
    if (err) { 
       throw err; 
    } else {
       if (row && row.length) {
	  console.log("Nmbr already exists")
       } else {
          var sql='INSERT INTO allow SET ?';
          db.query(sql, nmbr, function (err, data) {
             if (err) throw err;
          });
       }
    }
  });
  res.redirect('/callid/allow'); // redirect to the allow table
});
module.exports = router;

router.get('/allow/delete/:id', function(req, res, next) {
  const id = req.params;
  var sql='DELETE FROM allow WHERE ID= ?';
  db.query(sql, req.params.id, function (err, data) {
    if (err) throw err;
  });
  res.redirect('/callid/allow'); // redirect to the allow table
});
module.exports = router;
