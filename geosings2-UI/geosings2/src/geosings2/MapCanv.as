package geosings2
{
	import flash.display.CapsStyle;
	import flash.display.JointStyle;
	import flash.display.LineScaleMode;
	import flash.display.Sprite;
	
	import mx.containers.Canvas;
	import mx.core.UIComponent;
	import flash.display.Graphics;

	

	public class MapCanv extends Canvas
	{
		
		//private var UI:UIComponent = new UIComponent();
		
		public function MapCanv()
		{
			//TODO: implement function
			super();

			var dc: Graphics = this.graphics;
			dc.clear();
			dc.lineStyle(10, 0xFFD700, 10, false, LineScaleMode.VERTICAL,
                               CapsStyle.NONE, JointStyle.MITER, 10);


			dc.moveTo(0,0);
			dc.lineTo(300,300);
			dc.drawCircle(0,33,33);

			this.setFocus();
			//setStyle("backgroundColor","#ffffff");
		}
		
	}
}