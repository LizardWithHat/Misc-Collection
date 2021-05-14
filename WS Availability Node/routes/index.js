var express = require('express');
var router = express.Router();
var wol = require('node-wol');
const util = require('util');
const exec = util.promisify(require('child_process').exec);

async function query_pc(computer){
	var result = "";
	let stdout = await exec(`powershell.exe -Command "query user /server:${computer}"`).catch((err) => {
		result += err.stderr.toString();
		result += err.stdout.toString();
	});
	return result;
}

async function wake_up_pc(computer_mac){
	var result = 0; // Exit Code 0 => Success
	wol.wake(computer_mac, function(error){
		console.log(error);
		result = 1; //Exit Code not 0 => Error occured
	});
	return result;
}

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Server-04 Landing Page' });
});

router.get('/query_pc', async function(req, res){
	var computer = "vap01";
	var jsonObject = {};
	if (!(req.query.computer === undefined)){
		computer = req.query.computer;
	}
	jsonObject["message"] = await query_pc(computer);
    res.setHeader('Content-Type', 'application/json');
	res.send(jsonObject);
});

router.get('/wake_up_pc', async function(req, res){
	var computer_mac = req.query.computer_mac;
	var jsonResult = {};
	if(computer_mac === undefined){
		res.status(400);
		jsonResult["message"] = 'No MAC recieved'
	} else {
		if(wake_up_pc(computer_mac) === 1){
			res.status(500);
			jsonResult["message"] = 'Error waking up PC';
		} else {
			res.status(200);
			jsonResult["message"] = 'Successfully send wakeup package';
		}
	}
    res.setHeader('Content-Type', 'application/json');
	res.json(jsonResult);
});

router.get('/available_ws', function(req, res, next){
	var timeNow = new Date().toLocaleString();
	// This dict determines which computers will be queried. You can staticly list software here that will be displayed as well.
	var computer_dict = {	
	"computer01":[
	"Software A"
	], 
	
	"computer02":[
	"Software A"
	],
	
	"computer03":[
	"Software A",
	"Software B",
	"Software C"
	]};
	
	res.render('available_ws', { title: 'Availability of Workstations', time: timeNow, computers: computer_dict});
});

module.exports = router;