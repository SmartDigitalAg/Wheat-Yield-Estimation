import os
import rasterio
from rasterio.transform import from_origin
from rasterio.warp import reproject, Resampling

target_crs = 'EPSG:32652'

def resample_tif(input_path, output_path, target_resolution):
    with rasterio.open(input_path) as src_ds:
        transform = from_origin(src_ds.bounds.left, src_ds.bounds.top, target_resolution, target_resolution)
        width = int(src_ds.width * (src_ds.res[0] / target_resolution))
        height = int(src_ds.height * (src_ds.res[1] / target_resolution))

        kwargs = src_ds.meta.copy()
        kwargs.update({
            'crs': target_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        with rasterio.open(output_path, 'w', **kwargs) as dst_ds:
            reproject(
                source=rasterio.band(src_ds, 1),
                destination=rasterio.band(dst_ds, 1),
                src_transform=src_ds.transform,
                src_crs=src_ds.crs,
                dst_transform=transform,
                dst_crs=target_crs,
                resampling=Resampling.nearest
            )



def main():
    target_resolution = 250

    dataname_dict = {'3_lai': '500m', '4_lst': '1km'}

    for key, size in dataname_dict.items():
        base_dir = rf"D:\DATA\wheat\1_inputdata\{key}"
        output_dir = rf"D:\DATA\wheat\1_inputdata\out_{key.split('_')[1]}"


        file_list = [filename for filename in os.listdir(base_dir) if filename.endswith("tif")]

        for filename in file_list:
            input_filename = os.path.join(base_dir, filename)

            output_filename = os.path.join(output_dir, filename.replace(size, "250m"))
            resample_tif(input_filename,
                         output_filename, target_resolution)


if __name__ == '__main__':
    main()


# data = rio.open().data[:, :-1]