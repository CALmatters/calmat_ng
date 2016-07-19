<?
$iframes = array(
	array(75, "20151203_highway/roads"), 
	array(75, "20151203_highway/traffic"), 
	array(95, "20151119_cpm-map"), 
	array(65, "20150716_cap-and-trade-map"), 
	array(70, "20150709_greenhouse"),
	array(75, "20150708_greenhouse-policies"),
	array(80, "20150702_tomsteyer"), 
);
$servers = array(
	'external' => 'http://ext.calmatters.org',
	'calmatters.org' => '',
);
$server_chosen = (isset($_GET['server']) && array_key_exists($_GET['server'], $servers)) ? $_GET['server'] : "";
?>
<html>
<body style="background-color:orange;">
<form>
	Where will the iframe be displayed? 
	<select name="server">
		<? foreach($servers as $key=>$value) { ?>
			<option value="<?=$key?>" <? if($server_chosen == $key) { ?>selected<? } ?>><?=$key?></option>
		<? } ?>
	</select>
	<input type="submit" value="Go!" />
</form>
<? if($server_chosen == "") exit(); ?>
<hr />
<div style="float:left; max-width:5%;">Scroll down to see all iframes.</div>
<div style="float:left; max-width:80%; border-left:1px solid #333; padding-left:5px;">
	<?
	foreach($iframes as $framearray) {
		$iframe_str = '<div style="width: 100%; max-width: 100%; position: relative; padding-top: ' . $framearray[0] . '%;">' . "\n"
			. '<iframe src="' . $servers[$server_chosen] . '/iframes/' . $framearray[1] . '/" style="position: absolute; top: 0px; left: 0px; width: 100%; height: 100%;"></iframe>' . "\n"
			. '</div>' . "\n";
		echo "<pre>";
		echo preg_replace("#>#", "&gt;", preg_replace("#<#", "&lt;", $iframe_str));
		echo "</pre>";
		echo $iframe_str;
		?>
		<br /><br /><br />
		<?
	}
	?>
</div>
<br clear="all" />

</body>
</html>
