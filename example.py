import copernicusmarine

copernicusmarine.subset(
    dataset_id="cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i",
    variables=["thetao"],
    start_datetime="2022-01-01T00:00:00",
    maximum_longitude=-100.17,
    minimum_latitude=-100,
    maximum_depth=1.0,
)
