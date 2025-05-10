document.getElementById('upload').addEventListener('change', handleFile);

function handleFile(e) {
  const file = e.target.files[0];
  const reader = new FileReader();

  reader.onload = function (event) {
    const data = new Uint8Array(event.target.result);
    const workbook = XLSX.read(data, { type: 'array' });
    const sheet = workbook.Sheets[workbook.SheetNames[0]];
    const json = XLSX.utils.sheet_to_json(sheet);
    processData(json);
  };

  reader.readAsArrayBuffer(file);
}

function getRemarks(percentage) {
  if (percentage >= 95) return "Outstanding";
  if (percentage >= 81) return "Excellent";
  if (percentage >= 71) return "Very Good";
  if (percentage >= 61) return "Good";
  if (percentage >= 51) return "Fair";
  if (percentage >= 41) return "Needs Improvement";
  return "Poor";
}

function processData(data) {
  data = data.map(row => {
    const math = parseFloat(row['math score']) || 0;
    const reading = parseFloat(row['reading score']) || 0;
    const writing = parseFloat(row['writing score']) || 0;
    const percentage = ((math + reading + writing) / 3).toFixed(2);

    let grade = 'F';
    if (percentage >= 95) grade = 'O';
    else if (percentage >= 81) grade = 'A';
    else if (percentage >= 71) grade = 'B';
    else if (percentage >= 61) grade = 'C';
    else if (percentage >= 51) grade = 'D';
    else if (percentage >= 41) grade = 'E';

    const remarks = getRemarks(percentage);

    return { ...row, Percentage: percentage, Grade: grade, Remarks: remarks };
  });

  data.sort((a, b) => b.Percentage - a.Percentage);
  renderTable(data);
  renderCharts(data);
}

function renderTable(data) {
  const output = document.getElementById('output');
  const headers = Object.keys(data[0]);
  let html = '<table><thead><tr>' + headers.map(h => `<th>${h}</th>`).join('') + '</tr></thead><tbody>';

  data.forEach(row => {
    html += '<tr>' + headers.map(h => `<td>${row[h]}</td>`).join('') + '</tr>';
  });

  html += '</tbody></table>';
  output.innerHTML = html;
}

function renderCharts(data) {
  const grades = {};
  data.forEach(row => {
    grades[row.Grade] = (grades[row.Grade] || 0) + 1;
  });

  const avgMath = data.reduce((sum, r) => sum + parseFloat(r['math score']), 0) / data.length;
  const avgReading = data.reduce((sum, r) => sum + parseFloat(r['reading score']), 0) / data.length;
  const avgWriting = data.reduce((sum, r) => sum + parseFloat(r['writing score']), 0) / data.length;

  new Chart(document.getElementById('gradeChart'), {
    type: 'bar',
    data: {
      labels: Object.keys(grades),
      datasets: [{
        label: 'Grade Distribution',
        data: Object.values(grades),
        backgroundColor: '#42a5f5'
      }]
    },
    options: {
      plugins: {
        legend: { display: false },
        title: { display: true, text: 'Grade Distribution', font: { size: 16 } }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  });

  new Chart(document.getElementById('averageChart'), {
    type: 'pie',
    data: {
      labels: ['Math', 'Reading', 'Writing'],
      datasets: [{
        label: 'Average Score',
        data: [avgMath, avgReading, avgWriting],
        backgroundColor: ['#ef5350', '#42a5f5', '#ffb74d']
      }]
    },
    options: {
      plugins: {
        title: { display: true, text: 'Average Scores by Subject', font: { size: 16 } }
      }
    }
  });
}
