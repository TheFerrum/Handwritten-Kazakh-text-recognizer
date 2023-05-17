class Marker {

  constructor(_size, _color) {
    this.size = _size;
    this.color = _color;
    this.marks = [];
    this.isDrawing = false;
  }
  setSize(newSize) {
    this.size = newSize;
  }

  setColor(newColor) {
    this.color = newColor;
  }

  startDrawing() {
    this.isDrawing = true;
    this.marks = [];
  }

  stopDrawing() {
    this.isDrawing = false;
  }

  draw(x, y) {
    if (this.isDrawing) {
      var mark = {
        x: x,
        y: y
      };
      this.marks.push(mark);
    }
  }

  displayMarkings() {
    strokeWeight(this.size);
    stroke(this.color);

    if (this.marks.length > 1) {
      for (var i = 1; i < this.marks.length; i++) {
        line(
          this.marks[i].x,
          this.marks[i].y,
          this.marks[i - 1].x,
          this.marks[i - 1].y
        );
      }
    }
  }
}