i1 = rgb2gray(imread('image24.tif'));
i1 = adapthisteq(i1);
i2 = i1;
imshow(i1);

iVeritcaledges = edge(i1, 'prewitt', 0.1, 'vertical');
mask = ones([40 1]);
iVeritcaledges  = imopen(iVeritcaledges, mask);

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
lastOne = [0 0];
for j = 1:size(iVeritcaledges, 2)
    for i = 1:size(iVeritcaledges, 1)
        if ((iVeritcaledges(i, j) == 1 || i == size(iVeritcaledges, 1)) && lastOne(2) == j && i-lastOne(1) > 1)
            if (i == size(iVeritcaledges, 1))
                iVeritcaledges(i, j) = 1;
            end
            for k=lastOne(1)+1:i-1
                iVeritcaledges(k, j) = 1;
            end
            lastOne = [0 0];
        end
        if (iVeritcaledges(i, j) == 1)
            lastOne = [i j];
            continue;
        end
    end
end
for j = size(iVeritcaledges, 2):-1:1
    for i = size(iVeritcaledges, 1):-1:1
        if (i==1 && lastOne(2) == j && lastOne(1)-i > 1)
            if (i == 1)
                iVeritcaledges(i, j) = 1;
            end
            for k=i+1:lastOne(1)-1
                iVeritcaledges(k, j) = 1;
            end
            lastOne = [0 0];
        end
        if (iVeritcaledges(i, j) == 1)
            lastOne = [i j];
            continue;
        end
    end
end
lastOne = [0 0];
% for i = 1:size(iVeritcaledges, 1)
%     for j = 1:size(iVeritcaledges, 2)
%         if ((iVeritcaledges(i, j) == 1) && lastOne(1) == i && j - lastOne(2) > 1 && j - lastOne(2) < 5)
%             for k=lastOne(2)+1:j-1
%                 iVeritcaledges(i, k) = 1;
%             end
%             lastOne = [0 0];
%         end
%         if (iVeritcaledges(i, j) == 1)
%             lastOne = [i j];
%             continue;
%         end
%     end
% end
iVeritcaledges = imerode(iVeritcaledges, [1 0 1]);
%imshow(iVeritcaledges);

im = iVeritcaledges;
imshow(im);
%CropBoxes(i2, im);