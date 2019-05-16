% convert vector to matrix
% z1=vec2mat(z1,1);
% create new matrix with 1D elements in diagonal of matrix
% %z1 = diag(z1);
y = [41,41,41;42,42,42;43,43,43];
x = [-93,-93.5,-94;-93,-93.5,-94;-93,-93.5,-94;];
z = [32,31,30;27,0,20;10,5,3];
geoshow(y,x,z,'DisplayType','texturemap');
view(3);