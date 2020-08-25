import tensorflow as tf

print("Version : {}".format(tf.__version__))

# MNISTデータセットを使用
mnist = tf.keras.datasets.mnist
(x_train, t_train), (x_test, t_test) = mnist.load_data()
# 0~1へ正規化する
x_train, x_test = x_train / 255., x_test / 255.
print(x_train.shape, x_test.shape, t_train.shape, t_test.shape)

# 1.モデルの構築
model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28), name='inputs'),
  tf.keras.layers.Dense(128, activation='relu', name='relu'),
  tf.keras.layers.Dense(10, activation='softmax', name='softmax')
], name='Sequential')
# 2.モデルのコンパイル
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
# 3.モデルの学習
history = model.fit(x_train, t_train, epochs=5, batch_size=32)
# 4.モデルの評価
model.evaluate(x_test,  t_test, verbose=1)
# 5.モデルの保存(シリアル化)
model.save('Sequential_model')
# モデルの読み込み
model_load = tf.keras.models.load_model('Sequential_model')
# グラフの可視化
tf.keras.utils.plot_model(model, to_file='Sequetial.png', show_shapes=True)