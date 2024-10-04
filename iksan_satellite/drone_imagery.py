import os
import geopandas as gpd
import rasterio
import numpy as np
import pandas as pd
from rasterio.transform import from_origin
from rasterio.warp import reproject, Resampling

# target_crs = 'EPSG:4737'

def resample_tif(input_path, output_path, target_resolution):
    with rasterio.open(input_path) as src_ds:
        target_crs = src_ds.crs
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


def save_resampled_tir(root_dir, resampled_dir, target_resolutions):

    for target_resolution in target_resolutions:
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.tif') and 'resampled' not in file:

                    input_filename = os.path.join(root, file)
                    output_filename = os.path.join(resampled_dir, file.replace('.tif', f'_resampled{target_resolution}.tif'))
                    resample_tif(input_filename,
                                 output_filename, target_resolution)


def cal_vi(band_dct):

    blue_band, green_band, red_band, red_edge_band, nir_band = band_dct['blue'], band_dct['green'], band_dct['red'],band_dct['red_edge'], band_dct['nir']
    ndvi = (nir_band - red_band) / (nir_band + red_band)
    rvi = nir_band / red_band
    gndvi = (nir_band - green_band) / (nir_band + green_band)
    ndre = (nir_band - red_edge_band) / (nir_band + red_edge_band)
    cvi = (nir_band * red_band) / (green_band ** 2)
    return ndvi, rvi, gndvi, ndre, cvi


def process_vi(input_filename, output_filename):
    band_lst = ['blue', 'green', 'red', 'red_edge', 'nir']
    band_dct = {}
    with rasterio.open(input_filename) as src:
        for i in range(1, 6):
            band = src.read(i)
            no_data_value = band.min()
            band = np.where(band == no_data_value, np.nan, band)
            band_dct[band_lst[i - 1]] = band

    ndvi, rvi, gndvi, ndre, cvi = cal_vi(band_dct)
    with rasterio.open(input_filename) as src:
        kwargs = src.meta.copy()
        kwargs.update({
            'count': 5,
            'dtype': 'float32'
        })
        with rasterio.open(output_filename, 'w', **kwargs) as dst:
            dst.write(ndvi, 1)
            dst.write(rvi, 2)
            dst.write(gndvi, 3)
            dst.write(ndre, 4)
            dst.write(cvi, 5)


def get_plots_df(points, tiffile_path, output_csv_path):
    vi_bands = {'NDVI': 1, 'RVI': 2, 'GNDVI': 3, 'NDRE': 4, 'CVI': 5}

    with rasterio.open(tiffile_path) as src:
        affine = src.transform
        # VI 값 추출 함수
        def extract_vi_values(band_index, geometry):
            data = src.read(band_index)  # VI 밴드 읽기
            centroid = geometry.centroid
            x, y = centroid.x, centroid.y
            row, col = src.index(x, y)
            return data[row, col]

        # 각 지점에 대해 모든 VI 값 추출
        for vi_name, band_index in vi_bands.items():
            vi_values = []
            for geom in points.geometry:
                vi_value = extract_vi_values(band_index, geom) * 10
                vi_values.append(vi_value)
            points[vi_name] = vi_values

        # 'point_id'와 모든 VI 값만 포함하여 CSV 파일로 저장


    output_columns = ['geometry'] + list(vi_bands.keys())
    points[output_columns].to_csv(output_csv_path, index=False)


def stack_indices(tif_file, new_tif_file):
    with rasterio.open(tif_file) as src:
        red_band = src.read(1).astype(np.float32)
        blue_band = src.read(2).astype(np.float32)
        green_band = src.read(3).astype(np.float32)
        red_edge_band = src.read(4).astype(np.float32)
        nir_band = src.read(5).astype(np.float32)
        profile = src.profile

    # NDVI 계산
    ndvi = (nir_band - red_band) / (nir_band + red_band)

    # CVI 계산
    cvi = (nir_band / (red_band * green_band)) - 1

    # RVI 계산
    rvi = nir_band / red_band

    # GNDVI 계산
    gndvi = (nir_band - green_band) / (nir_band + green_band)

    # NDRE 계산
    ndre = (nir_band - red_edge_band) / (nir_band + red_edge_band)

    # 새로운 밴드를 데이터에 추가
    new_bands = np.stack([ndvi, cvi, rvi, gndvi, ndre])

    # 결과 저장
    with rasterio.open(new_tif_file, 'w', **profile) as dst:
        dst.write(new_bands)

def main():
    target_resolutions = [30, 10]
    root_dir = r"Z:\Projects\2311_디지털밀\데이터정리\드론촬영\드론영상"

    resampled_dir = os.path.join(root_dir, 'resampled')



    points_shp_path =  r"Z:\Projects\2311_디지털밀\데이터정리\드론촬영\샘플링위치shp\10sampling(surveying).shp"
    points = gpd.read_file(points_shp_path)

    tif_file = r"Z:\Projects\2311_디지털밀\데이터정리\드론촬영\드론영상\resampled\230130_iksan_hamra_resampled10.tif"
    new_tif_file = "output_tif_file.tif"

    stack_indices(tif_file, new_tif_file)

    with rasterio.open(new_tif_file) as src:
        # shp 파일의 각 centroid에 대해 식생지수 추출
        for index, row in points.iterrows():
            centroid = row.geometry.centroid.coords[0]
            lon, lat = centroid[0], centroid[1]

            # 픽셀값 추출
            x, y = src.index(lon, lat)
            ndvi_value = src.read(1, window=((y, y + 1), (x, x + 1)))

            # 추출된 픽셀값 출력 또는 저장
            print(f"Centroid ({lon}, {lat}): NDVI {ndvi_value[0][0]}")


    # tiffile_path = r"Z:\Projects\2311_디지털밀\데이터정리\드론촬영\드론영상\resampled\230130_iksan_hamra_resampled10.tif"
    # output_csv_path = 'test.csv'
    # get_plots_df(points, tiffile_path, output_csv_path)





if __name__ == '__main__':
    main()
