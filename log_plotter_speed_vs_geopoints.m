opts = detectImportOptions('Documents/logs/log_LAPS_CAN_2019_05_12_19_12_14.csv');
opts.SelectedVariableNames = [4 6 7];
m = readmatrix('Documents/logs/log_LAPS_CAN_2019_05_12_19_12_14.csv',opts);
m = m(logical(m(:,2)),:);
z1=m(:,1);
lat1=m(:,2);
lon1=m(:,3);
stem3(lon1,lat1,z1,'.');
grid on;
title('Speed VS Geopoints - Lap 1');
% z1=vec2mat(z1,1);
% %z1 = diag(z1);
% geoshow(lat1,lon1,z1);
% view(3);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%