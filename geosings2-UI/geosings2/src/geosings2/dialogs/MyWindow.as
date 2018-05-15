package geosings2.dialogs
{
	import mx.core.Window;

	public class MyWindow extends Window
	{
		public var parentWindow:Object;

		public function MyWindow()
		{
			super();
			this.systemChrome = "none"; //不显示系统窗口
			this.showStatusBar = false; //不显示底部状态栏
			this.showGripper = false; //不显示底部大小控制按钮
			this.showTitleBar = false;
			
		}
		
		/**
		* 自定义open()打开窗口并且保存调用此方法的对象
		*/
		public function advOpen(parentWindow:Object,openWindowActive:Boolean = true):void{
			this.parentWindow = parentWindow;
			this.open(true);
		}
		
	}
}