class Button {
  
  constructor(_x, _y, _radius) {
    this.x = _x;
    this.y = _y;
    this.radius = _radius;
  }
    
  displayButton() {
    fill(0);
    // noStroke();
    ellipseMode(CENTER);
    ellipse(this.x, this.y, this.radius);
    // strokeWeight(this.radius);
  }
    
}