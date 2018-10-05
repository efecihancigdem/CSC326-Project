<!DOCTYPE html>
<html>
<head>
<title>Kajima</title>
<style>
table {
}
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    padding: 15px;
    text-align: left;
}
table tr:nth-child(even) {
    background-color: #eee;
}
table tr:nth-child(odd) {
   background-color: #fff;
}
table th {
    background-color: black;
    color: white;
}
</style>
</head>

<body>


<img src="/image/kajima" alt="Kajima" usemap="#Logo" style="width:300px;height:150px;">

<!-- Dont forget to change w3schools -->
<map name="Logo">
  <area shape="rect" coords="0,0,300,150" alt="Kajima" href="http://127.0.0.1:8080/">
</map>

</body>

<h1> Your Research Results by Kajima </h2>

<p> You searched: <i>"{{query}}"</i> </p>

<h1> Search Results </h1>
<table id="results">
  <tr>
    <th>Word</th>
    <th>Count</th>
  </tr>
%for x in range(len(name)):
  <tr>
    <td>{{name[x]}}</td>
    <td>{{freq[x]}}</td>
  </tr>
%end
</table>

<p>Please click Kajima logo or <a href="http://127.0.0.1:8080/">here</a> to go back to home page </p>


</html>
