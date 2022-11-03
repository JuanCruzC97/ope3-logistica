import pandas as pd

def preparar_df_pedidos(df_pedidos, pedido):
    """
    Prepara el set de datos df_pedidos para el ruteo.

    Args:
        df_pedidos (pd.DataFrame): Dataframe con clientes y pedidos varios.
        pedido (str): Nombre de columna de df_pedidos con el pedido que queremos rutear.

    Returns:
        pd.DataFrame: _description_
    """
    df_pedido = (df_pedidos
                 [["cliente", pedido, "coord_x", "coord_y"]]
                 .rename({pedido:"pedidos"}, axis=1))

    return df_pedido