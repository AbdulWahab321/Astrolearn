class CanvasShapeRenderer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.shapes = [];
        this.defaultValues = {
            circle: { cx: 200, cy: 150, r: 50, fill: 'currentColor', stroke: 'currentColor', strokeWidth: 1 },
            ellipse: { cx: 200, cy: 150, rx: 75, ry: 50, fill: 'currentColor', stroke: 'currentColor', strokeWidth: 1 },
            rect: { x: 150, y: 100, width: 100, height: 100, fill: 'currentColor', stroke: 'currentColor', strokeWidth: 1 },
            line: { x1: 100, y1: 100, x2: 300, y2: 200, stroke: 'currentColor', strokeWidth: 1 },
            polyline: { points: '0,0 100,100 200,0', fill: 'none', stroke: 'currentColor', strokeWidth: 1 },
            polygon: { points: '100,100 200,100 150,200', fill: 'currentColor', stroke: 'currentColor', strokeWidth: 1 },
            path: { d: 'M150 0 L75 200 L225 200 Z', fill: 'currentColor', stroke: 'currentColor', strokeWidth: 1 },
            text: { x: 200, y: 150, text: 'Sample Text', font: '20px Arial', fill: 'currentColor', stroke: 'currentColor', strokeWidth: 1 },
            angle: { x: 200, y: 150, radius: 50, startangle: 0, endangle: 90, angle:30, fill: 'rgba(128,128,128,0.1)', stroke: 'currentColor', strokeWidth: 1 }
        };
        this.updateThemeColors();

        window.addEventListener('themeChanged', () => {
            this.updateThemeColors();
            this.render();
        });
    }

    updateThemeColors() {
        const computedStyle = getComputedStyle(document.body);
        this.themeColors = {
            backgroundColor: computedStyle.getPropertyValue('--body-bg-color').trim(),
            textColor: computedStyle.getPropertyValue('--text-color-primary').trim(),
            linkColor: computedStyle.getPropertyValue('--link-color').trim()
        };
    }

    parseShapes(shapesData) {
        const shapeStrings = shapesData.trim().split(/>\s*</);
        shapeStrings.forEach(shapeString => {
            shapeString = shapeString.replace(/^<|>$/g, '').trim();
            const [shapeType, ...paramsParts] = shapeString.split(/\s+/);
            const params = paramsParts.join(' ');
            const shapeParams = this.parseParams(params);
            this.shapes.push({ type: shapeType.trim(), params: shapeParams });
        });
    }

    parseParams(paramsString) {
        const params = {};
        if (!paramsString) return params;
        
        if (paramsString.includes('=')) {
            paramsString.split(/\s+/).forEach(param => {
                const [key, value] = param.split('=');

                if (key && value) {
                    params[key] = value.replace(/['"]/g, '');
                }
            });
        } else if (paramsString.includes(':')) {
            paramsString.split(',').forEach(param => {
                const [key, value] = param.split(':');
                console.log(key,value)

                if (key && value) {
                    params[key.trim()] = isNaN(value.trim()) ? value.trim() : parseFloat(value);
                }
                console.log(params)
            });
        } else {
            params.value = isNaN(paramsString.trim()) ? paramsString.trim() : parseFloat(paramsString);
        }

        return params;
    }

    render() {
        this.updateThemeColors();
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.fillStyle = this.themeColors.backgroundColor;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        this.shapes.forEach(shape => {
            const defaultParams = this.defaultValues[shape.type] || {};
            const params = { ...defaultParams, ...shape.params };
            
            if (params.fill === 'currentColor') params.fill = this.themeColors.textColor;
            if (params.stroke === 'currentColor') params.stroke = this.themeColors.textColor;

            this.drawShape(shape.type, params);
        });
    }

    drawShape(type, params) {
        switch (type) {
            case 'circle': this.drawCircle(params); break;
            case 'ellipse': this.drawEllipse(params); break;
            case 'rect': this.drawRect(params); break;
            case 'line': this.drawLine(params); break;
            case 'polyline': this.drawPolyline(params); break;
            case 'polygon': this.drawPolygon(params); break;
            case 'path': this.drawPath(params); break;
            case 'text': this.drawText(params); break;
            case 'angle': this.drawAngle(params); break;
        }
    }

    applyStyleAndDraw(params, drawFunc) {
        this.ctx.beginPath();
        drawFunc();
        if (params.fill !== 'none' && params.hollow !== 'true') {
            this.ctx.fillStyle = params.fill;
            this.ctx.fill();
        }
        if (params.stroke !== 'none') {
            this.ctx.strokeStyle = params.stroke;
            this.ctx.lineWidth = params.strokeWidth;
            this.ctx.stroke();
        }
    }

    drawCircle(params) {
        this.applyStyleAndDraw(params, () => {
            this.ctx.arc(params.cx, params.cy, params.r, 0, 2 * Math.PI);
        });
    }

    drawEllipse(params) {
        this.applyStyleAndDraw(params, () => {
            this.ctx.ellipse(params.cx, params.cy, params.rx, params.ry, 0, 0, 2 * Math.PI);
        });
    }

    drawRect(params) {
        this.applyStyleAndDraw(params, () => {
            this.ctx.rect(params.x, params.y, params.width, params.height);
        });
    }

    drawLine(params) {
        this.applyStyleAndDraw(params, () => {
            this.ctx.moveTo(params.x1, params.y1);
            this.ctx.lineTo(params.x2, params.y2);
        });
    }

    drawPolyline(params) {
        const points = params.points.split(' ').map(pair => pair.split(',').map(Number));
        this.applyStyleAndDraw(params, () => {
            this.ctx.moveTo(points[0][0], points[0][1]);
            for (let i = 1; i < points.length; i++) {
                this.ctx.lineTo(points[i][0], points[i][1]);
            }
        });
    }

    drawPolygon(params) {
        const points = params.points.split(' ').map(pair => pair.split(',').map(Number));
        this.applyStyleAndDraw(params, () => {
            this.ctx.moveTo(points[0][0], points[0][1]);
            for (let i = 1; i < points.length; i++) {
                this.ctx.lineTo(points[i][0], points[i][1]);
            }
            this.ctx.closePath();
        });
    }

    drawPath(params) {
        this.applyStyleAndDraw(params, () => {
            const path = new Path2D(params.d);
            this.ctx.fill(path);
            this.ctx.stroke(path);
        });
    }

    drawText(params) {
        this.ctx.font = params.font;
        this.ctx.fillStyle = params.fill;
        this.ctx.strokeStyle = params.stroke;
        this.ctx.lineWidth = params.strokeWidth;
        this.ctx.textAlign = params.textAlign || 'start';
        this.ctx.textBaseline = params.textBaseline || 'alphabetic';
        
        if (params.stroke !== 'none') {
            this.ctx.strokeText(params.text, params.x, params.y);
        }
        if (params.fill !== 'none') {
            this.ctx.fillText(params.text, params.x, params.y);
        }
    }

    drawAngle(params) {
        // Check for the 'angle' variable and calculate start and end angles
        if (params.angle !== undefined) {
            params.startangle = 180;
            params.endangle = params.angle;
        }
    
        // Convert angles from degrees to radians
        const startRad = (params.startangle * Math.PI) / 180;
        const endRad = (params.endAngle * Math.PI) / 180;
    
        // Ensure the angle is between 0 and -270 degrees (measured clockwise from the positive x-axis)
        const adjustedEndRad = (params.endAngle <= 0 && params.endAngle >= -270) ? endRad : (endRad - 2 * Math.PI);
    
        // Draw the arc representing the angle
        this.applyStyleAndDraw(params, () => {
            this.ctx.beginPath();
            this.ctx.moveTo(params.x, params.y); // Move to the center of the circle
            this.ctx.arc(params.x, params.y, params.radius, startRad, adjustedEndRad);
            this.ctx.stroke();
            this.ctx.closePath();
        });
    
        // Draw the sides of the angle with specified lengths
        const startX = params.x + params.sideLength1 * Math.cos(startRad);
        const startY = params.y + params.sideLength1 * Math.sin(startRad);
        const endX = params.x + params.sideLength2 * Math.cos(adjustedEndRad);
        const endY = params.y + params.sideLength2 * Math.sin(adjustedEndRad);
    
        this.ctx.beginPath();
        this.ctx.moveTo(params.x, params.y);
        this.ctx.lineTo(startX, startY); // Draw the first side
        this.ctx.moveTo(params.x, params.y);
        this.ctx.lineTo(endX, endY); // Draw the second side
        this.ctx.stroke();
    
        // Calculate the label position facing the top-right
        const labelRadius = params.radius * 1.2; // Position label slightly outside the arc
        const labelAngle = (params.startAngle + params.endAngle) / 2; // Midpoint angle
        const labelRad = (labelAngle * Math.PI) / 180; // Convert midpoint angle to radians
    
        const labelX = params.x + labelRadius * Math.cos(labelRad);
        const labelY = params.y + labelRadius * Math.sin(labelRad);
    
        // Draw the label
        this.ctx.fillStyle = this.themeColors.textColor; // Set text color
        this.ctx.font = '12px Arial'; // Set font properties
        this.ctx.textAlign = 'center'; // Center the text horizontally
        this.ctx.textBaseline = 'middle'; // Center the text vertically
        this.ctx.fillText(`${params.endAngle - params.startAngle}°`, labelX, labelY); // Draw the text
    }
    
}
// Initialize and use the CanvasShapeRenderer
document.addEventListener('DOMContentLoaded', () => {
    const canvasContainers = document.querySelectorAll('.canvas-container');
    canvasContainers.forEach((container, index) => {
        const canvas = document.createElement('canvas');
        canvas.id = `canvas-${index}`;
        canvas.width = 400;  // Default width, adjust as needed
        canvas.height = 300; // Default height, adjust as needed
        container.appendChild(canvas);

        const renderer = new CanvasShapeRenderer(`canvas-${index}`);
        renderer.parseShapes(container.innerHTML);
        renderer.render();

        // Clear the original HTML content
        container.innerHTML = '';
        container.appendChild(canvas);
    });
});

// Function to toggle theme (this should be called by your existing theme toggle function)
function toggleTheme() {
    document.body.classList.toggle('dark');
    window.dispatchEvent(new Event('themeChanged'));
}