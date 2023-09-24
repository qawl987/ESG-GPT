import imageio

# Create an array of image filenames
filenames = ['01_dow_1_85_company vs. average.png', '02_agilent_1_106_company vs. average.png', '03_amazon_1_79_company vs. average.png', '04_apple_1_72_company vs. average.png', '05_boeing_1_66_company vs. average.png', '06_bxp_1_65_company vs. average.png', '07_charles_1_50_company vs. average.png', '08_cisco_1_56_company vs. average.png', '09_citigroup_1_137_company vs. average.png', '10_cme_1_34_company vs. average.png', '11_colgate_1_84_company vs. average.png', '12_corning_1_71_company vs. average.png', '13_expeditor_1_37_company vs. average.png', '14_eei_1_80_company vs. average.png', '15_itt_1_44_company vs. average.png', '16_fedex_1_34_company vs. average.png', '17_firstscolar_1_57_company vs. average.png', '18_google_1_14_company vs. average.png', '19_intel_1_86_company vs. average.png', '20_jpmorgan_1_61_company vs. average.png', '21_microsoft_1_89_company vs. average.png', '22_rockwell_1_58_company vs. average.png', '23_ibm_1_49_company vs. average.png', '24_traveler_1_147_company vs. average.png', '25_visa_1_52_company vs. average.png']
# filenames = ['01_umc_1_154_company vs. average.png', '02_tsmc_1_210_company vs. average.png', '03_macronix_1_114_company vs. average.png', '04_esun_1_154_company vs. average.png', '05_eme_1_46_company vs. average.png', '06_asus_1_108_company vs. average.png', '07_acer_1_127_company vs. average.png', '08_witron_1_93_company vs. average.png', '09_honhai_1_22_company vs. average.png', '10_compal_1_169_company vs. average.png', '11_quanta_1_123_company vs. average.png', '12_formosa_1_18_company vs. average.png', '13_csc_1_150_company vs. average.png', '14_qisda_1_134_company vs. average.png', '15_msi_1_97_company vs. average.png', '16_gigabyte_1_74_company vs. average.png', '17_nanya_1_154_company vs. average.png', '18_novatek_1_140_company vs. average.png', '19_mediatek_1_97_company vs. average.png', '20_asia_1_119_company vs. average.png', '21_cathay_1_52_company vs. average.png', '22_cht_1_79_company vs. average.png', '23_fubon_1_89_company vs. average.png', '24_mega_1_68_company vs. average.png', 'average.png', 'company vs. average.png']
# Create an array of images
images = []
# nation = 'taiwan'
nation = 'american'
path = f'./png/{nation}/five/'
for filename in filenames:
    filepath = path + filename
    images.append(imageio.v3.imread(filepath))

# Save the images as a GIF animation
imageio.mimsave(f'{path}/{nation}.gif', images, duration=0.5)