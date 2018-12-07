<!DOCTYPE html>
	<html>
		<head>
			<link rel="shortcut icon" type="image/x-icon" href="/img/favicon.ico" />
			<title>Kajima | ABOUT </title>
			<link rel="stylesheet" type="text/css" href="./css/style.css">
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
						<li>
							<a href=/> Home</a>
						</li>
						<li class = "current">
							<a href=/about> About</a>
						</li>
					</ul>
					</nav>	
				</div>
			</header>
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
			<section id= "authors">
				<div class = "container">
					<article id= "main-col">
						<h1 class = "page-title">About Us</h1>
							<div class = "dark_box">
							<h3> Efe Cihan Cigdem </h3>
							<p>4th year ECE student from UofT. He always wants to go to gym but never does. His favourite sport is archery and he competed in Turkish national championship and he was not the first from the last. He loves coding
							as long as there is no bug or error.</p>
							</div>
							<div class = "box">
							<h3> Brandon</h3>
							<p>3rd year ECE student from UofT. Loves cooking, proponent for anti-realism with instrumentalist views. Believes all engineers should be instrumentalists. Has a kitchen knife collection.
							Mainly did backend for this website.</p>
							</div>
					</article>
					
				</div>
			</section>
		<footer>
			<p> Kajima, Copyright &copy; 2018</p>
		</footer>	
		</body>
	</html>