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
table#history tr:nth-child(even) {
    background-color: #eee;
}
table#history tr:nth-child(odd) {
   background-color: #fff;
}
table#history th {
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

<h2> Welcome to Kajima </h2>

<form action="/" method="post">
<p>Input your search here: <p> <input name="search" type="text" >
<input type="submit" value="submit">
</form>


<h2> Search History </h2>
<table id="history">
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



</html>
