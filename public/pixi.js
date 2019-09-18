var textOptions = {
    font: "14px Roboto", // Set  style, size and font
    fill: '#D3D3D3', // Set fill color to blue
    align: 'center' // Center align the text, since it's multiline
}

var stage = new PIXI.Container();
var graphics = new PIXI.Graphics();
var renderer = null;

function drawLevelLines(g,posX,posY,levelName,levelValue, valuePercentage, color) {
    const LEVEL_HEIGHT=200
    const LEVEL_WIDTH=50
    // Draw the container
    g.lineStyle(2, 0xD3D3D3, 1);
    g.moveTo(posX,posY);
    g.lineTo(posX, LEVEL_HEIGHT+posY);
    g.lineTo(LEVEL_WIDTH+posX, LEVEL_HEIGHT+posY);
    g.lineTo(LEVEL_WIDTH+posX, posY);

    // Print the label
    var labelText = new PIXI.Text(levelName,textOptions);
    labelText.anchor.x = 1;
    labelText.x = posX+labelText.width/2+LEVEL_WIDTH/2;
    labelText.y = LEVEL_HEIGHT+2+posY;
    g.addChild(labelText);

    // Print the value
    var labelText = new PIXI.Text(levelValue,textOptions);
    labelText.anchor.x = 1;
    labelText.x = posX+labelText.width/2+LEVEL_WIDTH/2;
    labelText.y = LEVEL_HEIGHT+20+posY;
    g.addChild(labelText);

    var labelText = new PIXI.Text(valuePercentage + "%",textOptions);
    labelText.anchor.x = 1;
    labelText.x = posX+labelText.width/2+LEVEL_WIDTH/2;
    labelText.y = LEVEL_HEIGHT+40+posY;
    g.addChild(labelText);

    // Calculate pixels from value (in %)
    var valueInPx = posY - LEVEL_WIDTH - levelValue*2
    // Draw the histogram (rectangle)
    g.beginFill(color, 1);
    g.drawRect(posX, LEVEL_HEIGHT+posY, LEVEL_WIDTH, valueInPx);
    g.endFill();
}

function setupLevelCanvas() {
    renderer = PIXI.autoDetectRenderer(
        800, 
        600, 
        { antialias: true, transparent: true });
    document.body.innerHTML = '';
    document.body.appendChild(renderer.view);
    stage.interactive = true;
    stage.addChild(graphics);
    console.log("rendered pixi");
}

function initLevels(values) {
    drawLevelLines(graphics,50,50,"Temperature",values['temperature'],values['temperaturePercentage'], 0xFF700B);
    drawLevelLines(graphics,150,50,"Moisture",values['moisture'],values['moisture'],0xFF700B);
    drawLevelLines(graphics,250,50,"Conductivity",values['conductivity'], values['conductivityPercentage'],0xFF700B);
    drawLevelLines(graphics,350,50,"Light",values['light'],values['lightPercentage'],0xFF700B);
    console.log("drew values");
    renderer.render(stage);
}