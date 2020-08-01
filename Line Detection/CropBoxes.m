function CropBoxes(im, mask)
    region = 1;
    finish = [0 0];
    count = 0;
    % Specify the folder where the files live.
    myFolder = 'Crops/';
    % Check to make sure that folder actually exists.  Warn user if it doesn't.
    if ~isfolder(myFolder)
        mkdir(myFolder);
    end
    % Get a list of all files in the folder with the desired file name pattern.
    filePattern = fullfile(myFolder, '*.tif'); % Change to whatever pattern you need.
    theFiles = dir(filePattern);
    for k = 1 : length(theFiles)
      baseFileName = theFiles(k).name;
      fullFileName = fullfile(myFolder, baseFileName);
      delete(fullFileName);
    end
    for i=1:size(im, 1)
        for j=1:size(im, 2)
           if (mask(i, j) >= 1)
               continue;
           end
           start = [i j];
           region = region+1;
           max = 0;
           for x=i:size(im, 1)
                if (mask(x, j) == 1 || x == size(im, 1))
                    for y=j:max
                        mask(x, y) = region;
                    end
                    finish = [x max];
                   break;
                end
                for y=j:size(im, 2)
                    if (mask(x, y) == 1 || y == size(im, 2))
                        mask(x, y) = region;
                        max = y;
                        break;
                    elseif (mask(x, y) == 0)
                        mask(x, y) = region;
                    end
                end
           end
           temp = zeros(finish(1)-start(1)+1, finish(2)-start(2)+1);
           for x=start(1):finish(1)
               for y=start(2):finish(2)
                   temp(x-start(1)+1, y-start(2)+1) = im(x, y);
               end
           end
           count = count+1;
           name = append('Crops/out_',int2str(count));
           name = append(name,'.tif');
           imwrite(uint8(temp), name);
        end
    end
end