i1 = rgb2gray(imread('image24.tif'));
i1 = adapthisteq(i1);
i2 = i1;
imshow(i1);

iHorizontaledges = edge(i1, 'Prewitt', 0.1, 'horizontal');
mask = ones([1 20]);
iHorizontaledges = imopen(iHorizontaledges, mask);

% mask = ones([3 3]);
% iHorizontaledges = imclose(iHorizontaledges, mask);
% mask = ones([1 500]);
% iHorizontaledges = imclose(iHorizontaledges, mask);
% for i=1:10
%     iHorizontaledges = imerode(iHorizontaledges, [1 1]);
% end
% for i=1:10
%     iHorizontaledges = imdilate(iHorizontaledges, [1 1]);
% end

%iedges = imdilate(iedges, [1 1 1 1 1 1 1 1 1 1 1 1]);
% iHorizontaledges = imerode(iHorizontaledges, [1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]);
% iHorizontaledges = imdilate(iHorizontaledges, [1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]);

lastOne = [0 0];
for i = 1:size(iHorizontaledges, 1)
    for j = 1:size(iHorizontaledges, 2)
        if ((iHorizontaledges(i, j) == 1 || j == size(iHorizontaledges, 2)) && lastOne(1) == i && j - lastOne(2) > 1)
            for k=lastOne(2):j
                iHorizontaledges(i, k) = 1;
            end
            lastOne = [0 0];
        end
        if (iHorizontaledges(i, j) == 1)
            lastOne = [i j];
            continue;
        end
    end
end

lastOne = [0 0];

for i = size(iHorizontaledges, 1):-1:1
    for j = size(iHorizontaledges, 2):-1:1
        if ((iHorizontaledges(i, j) == 1 || j == 1) && lastOne(1) == i && lastOne(2)-j > 1)
            for k=j:lastOne(2)
                iHorizontaledges(i, k) = 1;
            end
            lastOne = [0 0];
        end
        if (iHorizontaledges(i, j) == 1)
            lastOne = [i j];
            continue;
        end
    end
end

iHorizontaledges = iHorizontaledges + imerode(iHorizontaledges, [1; 0; 1]);
iHorizontaledges = imerode(iHorizontaledges, [1; 1; 1]);

% figure;
% imshow(iHorizontaledges);
% figure;
% imshow(iVeritcaledges);

% for i=1:10
%     iVeritcaledges = imerode(iVeritcaledges, [1; 1]);
% end
% for i=1:10
%     iVeritcaledges = imdilate(iVeritcaledges, [1; 1]);
% end
% iedges = imdilate(iedges, [1 1 1 1 1 1 1 1 1 1 1 1]);
% iVeritcaledges = imerode(iVeritcaledges, [1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1]);
% iVeritcaledges = imdilate(iVeritcaledges, [1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1]);

im = iHorizontaledges;
imshow(im);
imwrite(im, 'EdgesH');
%CropBoxes(i2, im);