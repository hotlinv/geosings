function load(){
//datastr = "{title:'图层s.p的信息',name:'s.p', path:'e:/s/p/a.shp', be:122.3, bw:123.3, bn:22.3, bs:11.2, wkt:'dfasdfsdf'}";
	var datastr = document.getElementById("conf").value;
	eval("var conf ="+ datastr) ;
	document.title = conf.title;
	//var win=new Ext.Window({title:"hello",width:300,height:200,html:'<h1>Hello,easyjf open source</h1>'});
	//win.show();

	
	var tabs = new Ext.TabPanel({
        renderTo: 'tabs1',
        width:600,
        activeTab: 0,
        frame:true,
        defaults:{autoHeight: true},
        items:[
            {contentEl:'baseinfo', title: '基本信息'},
            {contentEl:'spatial', title: '空间参考'},
            {contentEl:'attribute', title: '属性信息'}
        ]
    });
	
	var datab=[ [1, '','N:'+conf.bn,''],
		[2, 'W:'+conf.bw,'','E:'+conf.be], 
		[3, '','S:'+conf.bs,''] ];
	var storeb=new Ext.data.SimpleStore({data:datab,fields:['id',"ext1","ext2",'ext3']});
	var gridb = new Ext.grid.GridPanel({
		renderTo:"bound",
		title:"数据边缘",
		frame:false,
		enableColumnHide : true,
		trackMouseOver:false,
		columns:[{header:"",dataIndex:"ext1",align:"center"},
			{header:"",dataIndex:"ext2",align:"center"},
			{header:"",dataIndex:"ext3",align:"center"}],
		store:storeb
	}); 

	new Ext.Panel({
		renderTo:"base",
		title:conf.title,
		items:[{title:"名称",html:conf.name,height:100},
			{title:"路径",html:conf.path,height:100}
			]
		}
	);

    eval("var data = "+BASE64.decode(conf.fields));
	/*var data=[ [1, 'field1',"String"],
		[2, 'F2',"Int"], 
		[3, 'F3',"Real"],
		[4, 'f4',"String"] ];*/
	var store=new Ext.data.SimpleStore({data:data,fields:['id',"ext","extval",'width','prec']});
	var grid = new Ext.grid.GridPanel({
		renderTo:"fields",
		title:"属性表元数据",
		width:600, 
		columns:[{header:"列名",dataIndex:"ext",sortable:false},
			{header:"类型",dataIndex:"extval",sortable:false},
			{header:"宽度",dataIndex:"width",sortable:false},
			{header:"精度",dataIndex:"prec",sortable:false}
            ],
		store:store
	}); 

	
	new Ext.Panel({
		renderTo:"wkt",
		title:"空间参考(WKT)",
		html:BASE64.decode(conf.wkt)
	});
	
	//Ext.get('title1').update(conf.name);
	
}
