<!DOCTYPE html>
	<html>
		<head>
			<link rel="shortcut icon" type="image/x-icon" href="/img/favicon.ico" />
			<title>Kajima | Your search engine</title>
			<link rel="stylesheet" type="text/css" href="/css/style.css">
			<link rel="stylesheet" type="text/css" href="https://use.fontawesome.com/releases/v5.5.0/css/all.css">
		</head>
		<body>
			<header>
				<div class = "container">
					<div id = "branding">
						<h1> <span class = "highlight" >Kajima </span> Search Engine</h1>
					</div>	
					<nav>
					<ul>
						<li class = "current">
							<a href="http://127.0.0.1:8090/"> Home</a>
						</li>
						<li>
							<a href="http://127.0.0.1:8090/about"> About</a>
						</li>
					</ul>
					</nav>
				</div>
			</header>
			<section id = "showcase">
				<div class = "mode">
					%if logged_in==0:
						<a href="/signin" class="buttonz">
						Sign-in<br />
						<i class="fab fa-google"></i>
						</a>
					%else:
						<a href="/signout" class="buttonz">Sign Out<br />
						<i class="fab fa-google"></i>
						</a>
					%end
				</div>
				<div class = "container">
					<h1>Your Personal Search Engine</h1>
					<form action="/" method="get">
					<input name="keywords" type="text" placeholder="Enlighten Your World">
					<input type="submit" name = "engliht" class = "previous" value="Enlighten">
					<input type="submit" id = "lucky" name = "feeling_lucky" class = "previous" value="I am feeling lucky">
					</form>
				</div>
			</section>
		<footer>
			<p> Kajima, Copyright &copy; 2018</p>
		</footer>	
		</body>
	</html>
