import pandas as pd

from process_data import main as process_data
from teste_outlier import main as teste_outlier
from distributions import main as distributions
from k_coefficient import main as k_coefficient
from disaggregation_coef import main as disaggregation_coef
from ventechow import main as ventechow


def load_data():
    input_file_path = "python_app/csv/chuvas_C_01944009.csv"
    input_data = pd.read_csv(input_file_path, sep=";", encoding='ISO 8859-1', skiprows=12,
                             decimal=",", usecols=["NivelConsistencia", "Data", "Maxima"], index_col=False)

    gb_test_file_path = "python_app/csv/Tabela_Teste_GB.csv"
    gb_test = pd.read_csv(gb_test_file_path, sep=",",
                          encoding='ISO 8859-1', decimal=",", index_col=False)

    yn_sigman_file_path = "python_app/csv/Tabela_YN_sigmaN.csv"
    table_yn_sigman = pd.read_csv(yn_sigman_file_path, sep=",", encoding='ISO 8859-1',
                                  decimal=",", usecols=["Size", "YN", "sigmaN"], index_col=False)

    return input_data, gb_test, table_yn_sigman



def main():
    raw_df, gb_test, table_yn_sigman = load_data()

    processed_data = process_data(raw_df)
    
    no_outlier = teste_outlier(processed_data, gb_test)
    
    params, dist_r2 = distributions(
        no_outlier, table_yn_sigman)

    k_coefficient_data = k_coefficient(params, dist_r2)

    disaggregation_data, time_interval = disaggregation_coef(params, dist_r2)
    print(k_coefficient_data["k"])
    
    idf_data = ventechow(k_coefficient_data, disaggregation_data, params, time_interval, dist_r2)

    # Exportar idf_data para um arquivo JSON
    with open('node_app/src/idf_data.json', 'w') as f:
        f.write(idf_data.to_json(orient='records', lines=True))
        
    return idf_data


if __name__ == "__main__":
    main()
