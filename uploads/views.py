# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from django.shortcuts import render
from op_tasks.models import Experiment
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
import pandas
import numpy as np
import os

from models import Document
from forms import DocumentForm

@login_required(login_url='/tasking/login')
def expuploads(request):
    # Handle file uploads
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES, request.POST.get('dirName', 'error'))

        # redirect to the document after POST
        return HttpResponseRedirect(reverse('uploads.views.expuploads'))

    else:
        form = DocumentForm() # An empty, unbound form
        experiments = Experiment.objects.all()
        # Render list page with the documents and the form
        return render(request, 'expuploads.html', {'form': form, 'experiments': experiments})


def handle_uploaded_file(f, dirname):
    path = os.path.join('../static/results', dirname)
    try:
        os.makedirs(path)
    except OSError as e:
        print e
        print 'unable to create directory ' + path
    file = f['docfile']
    with open(path + '/' + file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # new code for parsing
    data = pandas.read_csv(path + '/' + file.name)
    cols = ['SYS.FIL.APP.','PST.EXP.CLD.CP.','PST.EXP.CLD.OT1.','PST.EXP.CLD.OT2.','PST.EXP.BED.CP.','PST.EXP.BED.OT1.',
        'PST.EXP.BED.OT2.','TSK.PRB.ANS.CP.','TSK.PRB.ANS.OT1.','TSK.PRB.ANS.OT2.','TSK.CON.CP.','TSK.CON.OT1.',
        'TSK.CON.OT2.','TSK.TIME.DIFF.CP.','TSK.TIME.DIFF.OT1.','TSK.TIME.DIFF.OT2.']
    workingData = data[cols]
    workingDataDF = pandas.DataFrame(workingData)
    workingDataDF[['PST.EXP.CLD.CP.','PST.EXP.CLD.OT1.','PST.EXP.CLD.OT2.','PST.EXP.BED.CP.','PST.EXP.BED.OT1.',
        'PST.EXP.BED.OT2.','TSK.PRB.ANS.CP.','TSK.PRB.ANS.OT1.','TSK.PRB.ANS.OT2.','TSK.CON.CP.','TSK.CON.OT1.',
        'TSK.CON.OT2.','TSK.TIME.DIFF.CP.','TSK.TIME.DIFF.OT1.','TSK.TIME.DIFF.OT2.']] = np.around(workingDataDF[['PST.EXP.CLD.CP.','PST.EXP.CLD.OT1.','PST.EXP.CLD.OT2.','PST.EXP.BED.CP.','PST.EXP.BED.OT1.',
        'PST.EXP.BED.OT2.','TSK.PRB.ANS.CP.','TSK.PRB.ANS.OT1.','TSK.PRB.ANS.OT2.','TSK.CON.CP.','TSK.CON.OT1.',
        'TSK.CON.OT2.','TSK.TIME.DIFF.CP.','TSK.TIME.DIFF.OT1.','TSK.TIME.DIFF.OT2.']], 0)

    tools = pandas.DataFrame(workingData['SYS.FIL.APP.']).drop_duplicates().sort('SYS.FIL.APP.').reset_index();
    del tools['index']
    tools.columns = ['Tools']
    tools.to_json(path_or_buf=path + '/' + "tools.json")


    metrics = {'load':{'col':'PST.EXP.CLD.CP.','max':5},
      'loadOT1':{'col':'PST.EXP.CLD.OT1.','max':5},
      'loadOT2':{'col':'PST.EXP.CLD.OT2.','max':5},
      'difficulty':{'col':'PST.EXP.BED.CP.','max':10},
      'difficultyOT1':{'col':'PST.EXP.BED.OT1.','max':10},
      'difficultyOT2':{'col':'PST.EXP.BED.OT2.','max':10},
      'performance':{'col':'TSK.PRB.ANS.CP.','max':10},
      'performanceOT1':{'col':'TSK.PRB.ANS.OT1.','max':10},
      'performanceOT2':{'col':'TSK.PRB.ANS.OT2.','max':10},
      'confidence':{'col':'TSK.CON.CP.','max':10},
      'confidenceOT1':{'col':'TSK.CON.OT1.','max':10},
      'confidenceOT2':{'col':'TSK.CON.OT2.','max':10},
      'time':{'col':'TSK.TIME.DIFF.CP.','max':10},
      'timeOT1':{'col':'TSK.TIME.DIFF.OT1.','max':10},
      'timeOT2':{'col':'TSK.TIME.DIFF.OT2.','max':10}}

    for key, value in metrics.items():
        df = pandas.DataFrame({key: workingDataDF.groupby(['SYS.FIL.APP.', value['col']], sort=0, as_index=False).size()}).reset_index()
        df.columns = ['Tool', 'Range', 'Count']
        df = df.sort(['Tool', 'Range'], ascending=[1, 1])
        array = []
        min = 1
        for i in tools.Tools:
            maxVal = int(value['max']) + 1
            for j in range(1,maxVal):
                subarray = [i, j]
                array.append(subarray)
        d = pandas.DataFrame(array, columns=('Tool', 'Range'))
        result = pandas.ordered_merge(df,d)
        result.to_csv(path_or_buf=path + '/' + str(key) + '.csv', sep=',',na_rep='0',index=False)