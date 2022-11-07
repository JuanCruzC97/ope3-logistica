import pandas as pd
from pathlib import Path

def preparar_df_pedidos(df_pedidos, pedido):
    """
    Prepara el set de datos df_pedidos para el ruteo.

    Args:
        df_pedidos (pd.DataFrame): Dataframe con clientes y pedidos varios.
        pedido (str): Nombre de columna de df_pedidos con el pedido que queremos rutear.

    Returns:
        pd.DataFrame: Dataframe de pedidos preparado para el ruteo.
    """
    df_pedido = (df_pedidos
                 [["cliente", pedido, "coord_x", "coord_y"]]
                 .rename({pedido:"pedidos"}, axis=1))

    return df_pedido

def load_inputs(sheet) -> pd.DataFrame:
    module_path: Path = Path(__file__)
    file_path: Path = (module_path / "../../data/inputs/data_inputs.xlsx").resolve()
    return pd.read_excel(file_path, sheet_name=sheet)