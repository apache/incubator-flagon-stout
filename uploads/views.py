from django.shortcuts import render
from op_tasks.models import Experiment
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

import pandas
import numpy as np

import os

from models import Document
from forms import DocumentForm

def list(request):
    # Handle file uploads
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES, request.POST.get('dirName', 'error'))

        # redirect to the document after POST
        return HttpResponseRedirect(reverse('uploads.views.list'))

    else:
        form = DocumentForm() # An empty, unbound form
        experiments = Experiment.objects.all()
        # Render list page with the documents and the form
        return render(request, 'list.html', {'form': form, 'experiments': experiments})

def handle_uploaded_file(f, dirname):
    path = os.path.join('../results/', dirname)
    try:
        os.mkdir(path)
    except:
        pass
    file = f['docfile']
    with open(path  + '/' + file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # new code for parsing
    data = pandas.read_csv(path + '/' + file.name)
    cols = ['SYS.FIL.APP.','PST.EXP.CLD.','PST.EXP.CLD.CP1.OT1.','PST.EXP.CLD.CP1.OT2.', 'PST.EXP.BED.', 'PST.EXP.BED.CP1.OT1.', 'PST.EXP.BED.CP1.OT2.']
    workingData = data[cols]
    workingDataDF = pandas.DataFrame(workingData)
    workingDataDF[['PST.EXP.CLD.','PST.EXP.CLD.CP1.OT1.','PST.EXP.CLD.CP1.OT2.', 'PST.EXP.BED.', 'PST.EXP.BED.CP1.OT1.', 'PST.EXP.BED.CP1.OT2.']] = np.around(workingDataDF[['PST.EXP.CLD.','PST.EXP.CLD.CP1.OT1.','PST.EXP.CLD.CP1.OT2.', 'PST.EXP.BED.', 'PST.EXP.BED.CP1.OT1.', 'PST.EXP.BED.CP1.OT2.']], 0)
    workingDataDF.head()

    tools = pandas.DataFrame(workingData['SYS.FIL.APP.']).drop_duplicates().sort('SYS.FIL.APP.').reset_index();
    del tools['index']
    tools.columns = ['Tools']

    metrics = {'load':{'col':'PST.EXP.CLD.','max':5},'loadOT1':{'col':'PST.EXP.CLD.CP1.OT1.','max':5}, 'loadOT2':{'col':'PST.EXP.CLD.CP1.OT2.','max':5},
    'difficulty':{'col':'PST.EXP.BED.','max':10}, 'difficultyOT1':{'col':'PST.EXP.BED.CP1.OT1.','max':10},'difficultyOT2':{'col':'PST.EXP.BED.CP1.OT2.','max':10}}

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
        result.to_csv(path_or_buf=path + str(key) + '.csv', sep=',',na_rep='0',index=False)