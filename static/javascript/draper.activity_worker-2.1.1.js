/* 
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 * 
 *   http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var logBuffer = [];
var loggingUrl = 'http://localhost:3001';
var intervalTime = 5000; //send every 5 seconds
var testing = false;
var echo = true;
var msg = 'DRAPER LOG: ';

function timerMethod() {

	if (logBuffer.length) {
    if (echo) {
      console.log(msg + 'sent ' + logBuffer.length + ' logs to - ' + loggingUrl)
    }
		if (!testing) {
			XHR(loggingUrl + '/send_log', logBuffer, function(d) {
				logBuffer = [];
			})			
		} else {
      logBuffer = [];
    }		
	}	else {
		if (echo) {
			console.log(msg + 'no log sent, buffer empty.')
		}		
	}
}

var timerId = setInterval(timerMethod, intervalTime);

self.addEventListener('message', function(e) {
  var data = e.data;
  switch (data.cmd) {
    case 'setLoggingUrl':
			loggingUrl = data.msg;
      break;
    case 'sendMsg':
      logBuffer.push(data.msg)
      break;
    case 'setTesting':
    	if (data.msg) {
    		var msg = 'DRAPER LOG: (TESTING) ';
    	} else {
    		var msg = 'DRAPER LOG: ';
    	}
      testing = data.msg;
      break;
    case 'setEcho':
      echo = data.msg;
      break;
    case 'sendBuffer':
    	sendBuffer();
    	break;
  };
}, false);


function sendBuffer() {
  // method to force send the buffer
	timerMethod();
	if (echo) {
		console.log(msg + ' buffer sent')
	}	
}
//simple XHR request in pure raw JavaScript
function XHR(url, log, callback) {
	var xhr;

	if(typeof XMLHttpRequest !== 'undefined') xhr = new XMLHttpRequest();
	else {
		var versions = ["MSXML2.XmlHttp.5.0", 
		 				"MSXML2.XmlHttp.4.0",
		 			  "MSXML2.XmlHttp.3.0", 
		 			  "MSXML2.XmlHttp.2.0",
		 				"Microsoft.XmlHttp"]

		 for(var i = 0, len = versions.length; i < len; i++) {
		 	try {
		 		xhr = new ActiveXObject(versions[i]);
		 		break;
		 	}
		 	catch(e){}
		 } // end for
	}
	
	xhr.onreadystatechange = ensureReadiness;
	
	function ensureReadiness() {
		if(xhr.readyState < 4) {
			return;
		}
		
		if(xhr.status !== 200) {
			return;
		}

		// all is well	
		if(xhr.readyState === 4) {
			callback(xhr);
		}			
	}
	
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	xhr.send(JSON.stringify(log));
}
