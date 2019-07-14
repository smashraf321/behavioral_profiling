opts = detectImportOptions('Documents/Smart Car/log_LAPS_CAN_2019_05_16_18_47_15.csv');
opts.SelectedVariableNames = [8 13];
m = readmatrix('Documents/Smart Car/log_LAPS_CAN_2019_05_16_18_47_15.csv',opts);
x1=m(:,2); %Distance
y1=m(:,1);%Speed
ax1 = subplot(4,1,1); % ax holds axes of current subplot
stopSign_img = imread('Documents/Smart Car/stop_sign_img.jpg');
%image(ax1,[2500,2600],[10,50],stopSign_img);
hold on; %to plot on the same figure
plot(ax1,x1,y1,'Color','blue');
title(ax1,'Speed VS Distance - Lap 1');
ylabel(ax1,'Speed (km/h)');
xlabel(ax1,'Distance (m)'); 
%xline(1430, '-',{'US 30 Entry Ramp'});
%xline(1800, '-');
rampIdx = find((x1>1430) & (x1<1800)); %get array of indices satisfying value in x1
rampX = x1(rampIdx); %get a sub array from x1 using the array of indices
rampY = y1(rampIdx);%get a subarray from y1
stop1Idx = find((x1>=30) & (x1<=70));
stop1X = x1(stop1Idx);
stop1Y = y1(stop1Idx);
stop2Idx =  find((x1>=2600) & (x1<=2800));
stop2X = x1(stop2Idx);
stop2Y = y1(stop2Idx);
stopLight1Idx = find( (x1>=2850) & (x1<=2970));
stopLight1X = x1(stopLight1Idx);
stopLight1Y = y1(stopLight1Idx);
stopLight1Plot = plot(ax1,stopLight1X,stopLight1Y,'Color','green');

stopLight2Idx = find( (x1>=5750) & (x1<=6000));
stopLight2X = x1(stopLight2Idx);
stopLight2Y = y1(stopLight2Idx);
stopLight2Plot = plot(ax1,stopLight2X,stopLight2Y,'Color','green');

stop1Plot = plot(ax1,stop1X,stop1Y,'Color','red');
stop2Plot = plot(ax1,stop2X,stop2Y,'Color','red');
rampPlot = plot(ax1,rampX,rampY,'Color','magenta'); %draw area curve on same axes and calculated X and Y series
%lines for ramp
area(ax1,rampX(1),rampY(1));
area(ax1,rampX(end),rampY(end));

%lines for stoplight2
area(ax1,stopLight2X(1),stopLight2Y(1));
area(ax1,stopLight2X(end),stopLight2Y(end));

%lines for stopSign2
area(ax1,stop2X(1),stop2Y(1));
area(ax1,stop2X(end),stop2Y(end));

legend([stop1Plot,rampPlot,stopLight1Plot,stopLight2Plot],{'stop sign','Ramp','Stop Light'});

hold off;
opts = detectImportOptions('Documents/Smart Car/log_LAPS_CAN_2019_05_16_19_05_17.csv');
opts.SelectedVariableNames = [8 13];
m = readmatrix('Documents/Smart Car/log_LAPS_CAN_2019_05_16_19_05_17.csv',opts);
x2=m(:,2);
y2=m(:,1);
ax2 = subplot(4,1,2);
plot(ax2,x2,y2,'Color','red');
title(ax2,'Speed VS Distance - Lap 2');
ylabel(ax2,'Speed (km/h)');
xlabel(ax2,'Distance (m)');
opts = detectImportOptions('Documents/Smart Car/log_LAPS_CAN_2019_05_16_19_21_09.csv');
opts.SelectedVariableNames = [8 13];
m = readmatrix('Documents/Smart Car/log_LAPS_CAN_2019_05_16_19_21_09.csv',opts);
x3=m(:,2);
y3=m(:,1);
ax3 = subplot(4,1,3);
plot(ax3,x3,y3,'Color','black');
title(ax3,'Speed VS Distance - Lap 3');
ylabel(ax3,'Speed (km/h)');
xlabel(ax3,'Distance (m)');
ax4 = subplot(4,1,4);
hold(ax4,'on');
plot(ax4,x1,y1,'Color','blue');
plot(ax4,x2,y2,'Color','red');
plot(ax4,x3,y3,'Color','black');
hold(ax4,'off');
title(ax4,'Speed VS Distance - Lap 1 vs 2 vs 3');
ylabel(ax4,'Speed (km/h)');
xlabel(ax4,'Distance (m)');