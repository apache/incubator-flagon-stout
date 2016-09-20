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
function toggle() {

  if ($("#ot_menu").hasClass('ot-show')) {
    $("#ot_menu").removeClass('ot-show');
    $("#ot_menu").addClass('ot-hide');

    $("#ot_menu .glyphicon").removeClass('glyphicon-chevron-down');
    $("#ot_menu .glyphicon").addClass('glyphicon-chevron-up');
    ac.logUserActivity('Closed menu', 'open-close', ac.WF_OTHER);
  } else {
    $("#ot_menu").removeClass('ot-hide');
    $("#ot_menu").addClass('ot-show');

    $("#ot_menu .glyphicon").removeClass('glyphicon-chevron-up');
    $("#ot_menu .glyphicon").addClass('glyphicon-chevron-down');
    ac.logUserActivity('Opened menu', 'open-close', ac.WF_OTHER);
  }
}

