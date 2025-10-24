def show_prediction_comparison(img, pred_mask):
    from matplotlib import pyplot as plt

    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    img.show(ctx=ax[0], title='Original Image')
    pred_mask.show(ctx=ax[1], title='Predicted Mask')
    plt.show()
