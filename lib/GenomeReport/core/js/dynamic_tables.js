// javascript
'use strict';

/* global d3 */

// Title div with label and button
const header = d3.select('body').append('div').attr('class', 'well');

header.append('h3').text('Dynamic D3 Array of Tables');

const taskLabel = header.append('label')
    .attr('id', 'taskLabel')
    .html('&nbsp;');

let currTask = 0;
const taskButton = header.append('button')
    .attr('class', 'btn btn-primary')
    .style('margin-bottom', '20px')
    .style('width', '100%')
    .style('text-align', 'left')
    .text('Start')
    .on('click', function() {
      this.blur();
      // Execute the task
      tasks[currTask]();
      // Next task
      currTask = ++currTask % tasks.length;
    });

// Container for array of tables
const tableDiv = d3.select('body').append('div').attr('id', 'tableContainer');

// Initial data
let data;
const initialData = [
    { table: 'Table1', rows: [
        { table: 'Table1', row: 'Row1', data: 'DataT1R1' },
        { table: 'Table1', row: 'Row2', data: 'DataT1R2' }
    ]
    },
    { table: 'Table2', rows: [
        { table: 'Table2', row: 'Row1', data: 'DataT2R1' },
        { table: 'Table2', row: 'Row2', data: 'DataT2R2' },
        { table: 'Table2', row: 'Row3', data: 'DataT2R3' }
    ]
    },
    { table: 'Table3', rows: [
        { table: 'Table3', row: 'Row1', data: 'DataT3R1' },
        { table: 'Table3', row: 'Row2', data: 'DataT3R2' }
    ]
    },
    { table: 'Table4', rows: [
        { table: 'Table4', row: 'Row1', data: 'DataT4R1' },
        { table: 'Table4', row: 'Row2', data: 'DataT4R2' }
    ]
    }
];

// Tasks
function task0() {
    // Clear any existing tables (by providing an empty array)
    update([]);

    taskLabel.html('Cleared any existing tables');
    taskButton.text('Next step: Initial load of tables');
}

function task1() {
    // Load initial tables
    data = JSON.parse(JSON.stringify(initialData));
    update(data);

    taskLabel.text('Step 1: Initial tables loaded');
    taskButton.text('Next step: Add 4th row to Table 2');
}

function task2() {
    // Add 4th row to table 2
    data[1].rows.push({ table: 'Table2', row: 'Row4', data: 'DataT2R4' });
    update(data);

    taskLabel.text('Step 2: Added 4th row to Table 2');
    taskButton.text('Next step: Delete first row of Table 3');
}

function task3() {
    // Delete first row of table 3
    data[2].rows.shift();
    update(data);

    taskLabel.text('Step 3: Deleted first row of Table 3');
    taskButton.text('Next step: Add Table 5 with 8 rows');
}

function task4() {
  // Add table 5 with 8 rows
    data.push({
        table: 'Table5', rows: [
            { table: 'Table5', row: 'Row1', data: 'DataT5R1' },
            { table: 'Table5', row: 'Row2', data: 'DataT5R2' },
            { table: 'Table5', row: 'Row3', data: 'DataT5R3' },
            { table: 'Table5', row: 'Row4', data: 'DataT5R4' },
            { table: 'Table5', row: 'Row5', data: 'DataT5R5' },
            { table: 'Table5', row: 'Row6', data: 'DataT5R6' },
            { table: 'Table5', row: 'Row7', data: 'DataT5R7' },
            { table: 'Table5', row: 'Row8', data: 'DataT5R8' }
        ]
    });
    update(data);

    taskLabel.text('Step 4: Added Table 5 with 8 rows');
    taskButton.text('Next step: Remove Table 4');
}

function task5() {
    // Remove table 4
    data.splice(3, 1);
    update(data);

    taskLabel.text('Step 5: Removed Table 4');
    taskButton.text('Next step: Change data of row 1 of Table 1');
}

function task6() {
    // Change the content of row 1 of table 1
    var item = data[0].rows[0].data;
    data[0].rows[0].data = item + ' - Updated';
    update(data);

    taskLabel.text('Step 6: Changed data of row 1 of Table 1');
    taskButton.text('Next step: Change order of tables');
}

function task7() {
    // Change the order of tables (move last table to first position)
    data.unshift(data.pop());
    d3.select('#tableContainer').selectAll('*').remove();
    update(data);

    taskLabel.text('Step 7: Changed order of tables');
    taskButton.text('Restart');
}

// Task list (array of functions)
var tasks = [task0, task1, task2, task3, task4, task5, task6, task7];

// Function in charge of the array of tables
function update(data) {

    // Select all divs in the table div, and then apply new data
    const divs = tableDiv.selectAll('div')
        // After .data() is executed below, divs becomes a d3 update selection
        .data(data, d => d.table);

    // Use the exit method of the d3 update selection to remove any deleted table div and contents (which would be absent in the data array just applied)
    divs.exit().remove();

    // Use the enter metod of the d3 update selection to add new ('entering') items present in the
    // data array just applied
    const divsEnter = divs
      .enter().append('div')
        .attr('id', d => `${ d.table }-Div`)
        .attr('class', 'well');

    // Add title in new div(s)
    divsEnter.append('h5').text(d => d.table);

    divs.selectAll('h5').text(d => `${ d.table }`);

    // Add table in new div(s)
    const tableEnter = divsEnter.append('table')
        .attr('id', d => d.table)
        .attr('class', 'table table-condensed table-striped table-bordered');

    // Append table head in new table(s)
    tableEnter.append('thead')
      .append('tr')
        .selectAll('th')
        // Table column headers (here constant, but could be made dynamic)
        .data(['Table Name', 'Row Number', 'Data Contents'])
      .enter().append('th')
        .text(d => d);

    // Append table body in new table(s)
    tableEnter.append('tbody');

    // Select all tr elements in the divs update selection
    const tr = divs.select('table').select('tbody').selectAll('tr')
      // After the .data() is executed below, tr becomes a d3 update selection
    .data(
        d =>  d.rows, // Return inherited data item
        d => d.row    // 'key' function to disable default by-index evaluation
    );

    // Use the exit method of the update selection to remove table rows without associated data
    tr.exit().remove();

    // Use the enter method to add table rows corresponding to new data
    tr.enter().append('tr');

    // Bind data to table cells (td becomes update selection)
    const td = tr.selectAll('td')
        // After the .data() is executed below, the td becomes a d3 update selection
        .data(d => d3.values(d));   // return inherited data item

    // Use the enter method of the update selection to add td elements
    td.enter().append('td');

    // Use the update selection to add/change the table cell text
    td.text(d => d);
}