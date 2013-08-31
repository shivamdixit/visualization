var pad = 15;
var w = 1180;
var h = 480;
var a = [];
for(var i =0;i<30;i++)
	a.push(Math.floor(Math.random()*100));
var svg = d3.select("body")
			.append("svg:svg")
			.attr("width",w)
			.attr("height",h)
			.style("margin-left",70+"px")
			.style("margin-top",30+"px")
			.style("background-fill","rgb(121,147,151)")
			.style("pointer-events", "all");
svg.append("g");
svg.append("a");
//scales and lines
var scale = d3.scale.linear()
				.domain([0,100])
				.range([0,450]);
var pseudoScale = d3.scale.linear()
				.domain([0,100])
				.range([450,0]);
var invScale = d3.scale.linear()
				.domain([0,450])
				.range([0,100]); 

svg.append("line")
	.attr("x1",27)
	.attr("y1",h-pad+3)
	.attr("x2",w)
	.attr("y2",h-pad+3)
	.attr("stroke","black")
	.style("shape-rendering","crispEdges");

//Axis

var axis = d3.svg.axis()
				.scale(pseudoScale)
				.orient("left")
				.ticks(5)
svg.append("g")
    .attr("class", "axis")
  	.attr("transform", "translate(" + 27 + ","+ (pad+3) + ")")
    .call(axis);
svg.append("rect")
	.attr("class","pop")
	.attr("fill","none")
	.attr("fill-opacity",0.85)
	.attr("width",160)
	.attr("height",45);
svg.append("text")
	.attr("class","popText")
	.attr("fill-opacity",0.95)
	.attr("fill","none")
	.attr("font-size",15)
	.attr("font-family","sans-serif");
	

//loading data for the first time
svg.select("a")
	.selectAll("rect")
	.data(a)
	.enter()
	.append("rect")
	.attr("x",function(d,i){
				return 20+i*((w-30)/a.length) + pad;
	})
	.attr("y",function(d){
				return h-scale(d)-(pad-3);
	})
	.attr("width",(w-30)/a.length - 17)
	.attr("height",function(d){
				return scale(d);
	})
	.attr("fill","green")
	.attr("fill-opacity",0.9)
	.on("mousemove", function() {
		console.log("mouseMoved")
        var x =	d3.mouse(this)[0];
       	var y =	d3.mouse(this)[1];
		var xPos,yPos;
		if ((x+210)<w)
	        xPos = x+25;
	    else
	       	xPos = (x+25)-(x+210-w);
	    if ((y-45)>0 && (y+30)<h)
	     	yPos = y-45;
	    else if((y+30)>h)
	        yPos = y-45 - (y+30-h+35);
	    else
	        yPos = 45-y;
		d3.select(this)
			.attr("fill-opacity",1.0) 
			.attr("stroke","black");
		d3.select(".pop")
	                .attr("fill", "rgb(230,240,210)")
	                .attr("x",xPos)
	                .attr("y",yPos);
		d3.select(".popText")
	                .attr("fill", "black")
	                .attr("x",xPos + 10)
	                .attr("y",yPos + 25)
					.text("Value : "+ Math.floor(invScale(d3.select(this).attr("height"))));
	})
	.on("mouseout", function() {
		d3.select(this)
			.attr("fill-opacity",0.9)
			.attr("stroke","none");
	        d3.selectAll(".pop")
	        		.attr("x",0)
	                .attr("y",999999);
		d3.selectAll(".popText")
	                .attr("fill", "none")
	                .text("")
	                .attr("x",0)
	                .attr("y",999999);
	
	})
	
function next(){
	var b=[];
	for(var i =0;i<30;i++)
		b.push(a[i]);
	a=[];

	for(var i =0;i<30;i++)
		a.push(Math.floor(Math.random()*100));
	var rect = d3.select("body")
					.select("svg")
					.select("a")
					.selectAll("rect")
      				.data(a);
    rect.enter()
    	.append("rect");
    rect.transition()
    	.duration(1500)
	   	.attr("x",function(d,i){
					return 20+i*((w-30)/a.length) + pad;
		})
		.attr("y",function(d){
					return h-scale(d)-(pad-3);
		})
		.attr("width",(w-30)/a.length - 17)
		.attr("height",function(d){
					return scale(d);
		})
		.attr("fill",function(d,i){
				if(d>b[i])
					return "green";
				else
					return "red";})
		.attr("fill-opacity",0.9)
		.attr("text",function(d){return d;});
	rect.exit().remove()
	var rect2 = d3.select("body")
					.select("svg")
					.select("g")
					.selectAll("rect")
      				.data(b);
    rect2.enter()
    	.append("rect");
    rect2.transition()
    	.duration(1200)
	   	.attr("x",function(d,i){
					return 17+i*((w-30)/a.length) - 3 + pad;
		})
		.attr("y",function(d){
					return h-scale(d)-(pad-3);
		})
		.attr("width",(w-30)/a.length - 5)
		.attr("height",function(d){
					return scale(d);
		})
		.attr("fill","black")			
		.attr("fill-opacity", 0.3);
	rect2.exit().remove()
}
//will execute next() after every 3 secs
var refresh;
function startRefresh(){
	document.getElementById("stp").disabled = false;
	document.getElementById("strt").disabled = true;
	refresh = setInterval(function(){next();},3000);

}
function stop(){
	document.getElementById("stp").disabled = true;
	document.getElementById("strt").disabled = false;
	clearInterval(refresh);
	
}