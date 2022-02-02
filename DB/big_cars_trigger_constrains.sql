use trafficcontrol;
 DELIMITER //
 create trigger update_heavy_car_control BEFORE UPDATE ON trafficcontrol.mainapp_car
FOR EACH ROW
 BEGIN

 IF (NEW.owner_id in (select owner_id from trafficcontrol.mainapp_car where car_type = "big") and NEW.car_type = "big" ) THEN
 signal sqlstate '45000'
 	SET MESSAGE_TEXT =  "Owner has a big car already";
 end if ;
 END //

 DELIMITER ;



DELIMITER //
create trigger insert_heavy_car_control BEFORE INSERT ON trafficcontrol.mainapp_car
FOR EACH ROW
BEGIN

IF (NEW.owner_id in (select owner_id from trafficcontrol.mainapp_car where car_type = "big") and NEW.car_type = "big" ) THEN
signal sqlstate '45000'
	SET MESSAGE_TEXT =  "Owner has a big car already";
end if ;
END //

DELIMITER ;