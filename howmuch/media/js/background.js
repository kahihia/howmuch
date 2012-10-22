$(function()
{
   

    if(document.createElement('canvas') && navigator && !(navigator.userAgent.match(/iPhone/i) || navigator.userAgent.match(/iPod/i) || navigator.userAgent.match(/iPad/i)))
    {
        function Bit(size, color){ //Propiedades de los cuadritos
            this.size = size;
            if (size < 40)
            {
                this.speed = 3;
            }
            else if(size < 60)
            {
                this.speed = 2;
            }
            else
            {
                this.speed = 1;
            }
            this.color = color;
            this.xpos = Math.random() * screen.availWidth - this.size; //Numero aleatorio entre 0 y el ancho de la pantalla menos el tamaño de Bit
            this.ypos = 100 + 500 * (canvas.width-this.xpos)/canvas.width + 100 * Math.tan(this.offset + this.xpos / 500);
            this.offset = 100 * Math.random(); //Numero Aleatorio entre 0 y 100
        }

        function tick(bit)
        {
            if(bit.xpos > maxX)
            {
                bit.xpos = -bit.size;
                bit.offset = new Number(100 * Math.random());
            }
            else
            {
                bit.xpos += bit.speed;
            }
            bit.ypos = 100 + 500 * (canvas.width-bit.xpos)/canvas.width + 100 * Math.sin(bit.offset + bit.xpos / 500);
            context.shadowColor = bit.color;
            context.fillStyle = bit.color;
            context.fillRect(bit.xpos, bit.ypos, bit.size, bit.size);
        }

        function reDraw()
        {
            context.clearRect(0,0,canvas.width, canvas.height);
            bits.map(tick);
        }

        document.body.style['background-color'] = 'white';
        document.body.style['background'] = 'white';
        var colours = ['green', 'blue', 'red', 'yellow'], //Colores de los cuadritos
            maxX = screen.availWidth + 40;
        var canvas = document.getElementById('background');
        canvas.width = screen.availWidth;
        canvas.height = 800;
        var context = canvas.getContext('2d');
        context.globalAlpha = 0.7;
        context.shadowBlur = 7;

        var bits = new Array(50);
        var bit;
        for(var i = 0; i < 50; ++i)
        {
            bit = new Bit(20 + 70 * Math.random(), colours[Math.floor(4 * Math.random())]);
            bits[i] = bit;
        }

        setInterval(reDraw, 50);

    }


});
