%--- Plot 1st Lap ---%
opts = detectImportOptions('Documents/logs/log_LAPS_2019_06_01_13_10_03.csv');
opts.SelectedVariableNames = [4 14];
m = readtable('Documents/logs/log_LAPS_2019_06_01_13_10_03.csv',opts);
x1=m{:,1};
y1=m{:,2};
% ax1 = subplot(5,1,1);
% plot(ax1,x1,y1,'Color','blue');
% title(ax1,'Distance VS Time - Lap 1');
% ylabel(ax1,'Distance (m)');
% xlabel(ax1,'Time (s)');
%--- Plot 2nd Lap ---%
opts = detectImportOptions('Documents/logs/log_LAPS_2019_06_01_13_28_04.csv');
opts.SelectedVariableNames = [4 14];
m = readtable('Documents/logs/log_LAPS_2019_06_01_13_28_04.csv',opts);
x2=m{:,1};
y2=m{:,2};
% ax2 = subplot(5,1,2);
% plot(ax2,x1,y1,'Color','red');
% title(ax2,'Distance VS Time - Lap 2');
% ylabel(ax2,'Distance (m)');
% xlabel(ax2,'Time (s)');
%--- Plot 3rd Lap ---%
opts = detectImportOptions('Documents/logs/log_LAPS_2019_06_01_13_45_49.csv');
opts.SelectedVariableNames = [4 14];
m = readtable('Documents/logs/log_LAPS_2019_06_01_13_45_49.csv',opts);
x3=m{:,1};
y3=m{:,2};
% ax3 = subplot(5,1,3);
% plot(ax3,x1,y1,'Color','black');
% title(ax3,'Distance VS Time - Lap 3');
% ylabel(ax3,'Distance (m)');
% xlabel(ax3,'Time (s)');
%--- Plot 4th Lap ---%
opts = detectImportOptions('Documents/logs/log_LAPS_2019_06_01_14_03_28.csv');
opts.SelectedVariableNames = [4 14];
m = readtable('Documents/logs/log_LAPS_2019_06_01_14_03_28.csv',opts);
x4=m{:,1};
y4=m{:,2};
% ax4 = subplot(5,1,4);
% plot(ax4,x1,y1,'Color','green');
% title(ax4,'Distance VS Time - Lap 4');
% ylabel(ax4,'Distance (m)');
% xlabel(ax4,'Time (s)');
%--- Plot all 4 laps together ---%
% ax5 = subplot(5,1,5);
% hold(ax5,'on');
% plot(ax5,x1,y1,'Color','blue');
% plot(ax5,x2,y2,'Color','red');
% plot(ax5,x3,y3,'Color','black');
% plot(ax5,x4,y4,'Color','green');
% hold(ax5,'off');
% title(ax5,'Distance VS Time - Lap 1 vs 2 vs 3 vs 4');
% ylabel(ax5,'Distance (m)');
% xlabel(ax5,'Time (s)');
%--- ---%
%--- only combined ---%
hold('on');
plot(x1,y1,'Color','blue');
plot(x2,y2,'Color','red');
plot(x3,y3,'Color','black');
plot(x4,y4,'Color','green');
hold('off');
%--- ---%
title('Distance VS Time - Lap 1 vs 2 vs 3 vs 4');
ylabel('Distance (m)');
xlabel('Time (s)');