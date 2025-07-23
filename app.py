from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import os
import subprocess
import uuid

app = Flask(__name__)
app.secret_key = 'secret_key'

DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/instagram')
def instagram():
    return render_template('instagram.html')

@app.route('/spotify')
def spotify():
    return render_template('spotify.html')

@app.route('/anghami')
def anghami():
    return render_template('anghami.html')

@app.route('/facebook')
def facebook():
    return render_template('facebook.html')


@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        flash("يرجى إدخال رابط صحيح.", "error")
        return redirect(url_for('index'))

    try:
        unique_id = str(uuid.uuid4())[:8]
        output_template = os.path.join(DOWNLOAD_FOLDER, f'%(title)s_{unique_id}.%(ext)s')
        command = [
            'yt-dlp',
            '-x', '--audio-format', 'mp3',
            '--embed-thumbnail',
            '--add-metadata',
            '-o', output_template,
            url
        ]

        subprocess.run(command, check=True)

        # البحث عن الملف الناتج بصيغة mp3
        for filename in os.listdir(DOWNLOAD_FOLDER):
            if filename.endswith('.mp3') and unique_id in filename:
                full_path = os.path.join(DOWNLOAD_FOLDER, filename)
                return send_file(full_path, as_attachment=True)

        flash("حدث خطأ أثناء حفظ الملف.", "error")
        return redirect(url_for('index'))

    except subprocess.CalledProcessError as e:
        flash(f"حدث خطأ أثناء التحويل: {str(e)}", "error")
        return redirect(url_for('index'))


@app.route('/download_instagram', methods=['POST'])
def download_instagram():
    url = request.form.get('url')
    if not url:
        flash("يرجى إدخال رابط صحيح.", "error")
        return redirect(url_for('instagram'))

    try:
        # هنا ممكن تستخدم yt-dlp أو مكتبة خاصة لإنستجرام
        unique_id = str(uuid.uuid4())[:8]
        output_template = os.path.join(DOWNLOAD_FOLDER, f'instagram_{unique_id}.%(ext)s')

        command = [
            'yt-dlp',
            '-o', output_template,
            url
        ]
        subprocess.run(command, check=True)

        # ابحث عن الملف الناتج (مثلاً الفيديو أو صورة)
        for filename in os.listdir(DOWNLOAD_FOLDER):
            if unique_id in filename:
                full_path = os.path.join(DOWNLOAD_FOLDER, filename)
                return send_file(full_path, as_attachment=True)

        flash("حدث خطأ أثناء حفظ ملف إنستجرام.", "error")
        return redirect(url_for('instagram'))

    except subprocess.CalledProcessError as e:
        flash(f"خطأ أثناء التحميل من إنستجرام: {str(e)}", "error")
        return redirect(url_for('instagram'))


@app.route('/download_spotify', methods=['POST'])
def download_spotify():
    url = request.form.get('url')
    if not url:
        flash("يرجى إدخال رابط صحيح.", "error")
        return redirect(url_for('spotify'))

    # ملاحظة: تحميل من Spotify معقد عادة ويحتاج API خاص أو خدمات خارجية
    # هذا مجرد مثال بسيط توضيحي:
    flash("تحميل Spotify غير مدعوم حالياً. سيتم تطويره لاحقاً.", "error")
    return redirect(url_for('spotify'))


@app.route('/download_anghami', methods=['POST'])
def download_anghami():
    url = request.form.get('url')
    if not url:
        flash("يرجى إدخال رابط صحيح.", "error")
        return redirect(url_for('anghami'))

    # مثال توضيحي فقط:
    flash("تحميل Anghami غير مدعوم حالياً. سيتم تطويره لاحقاً.", "error")
    return redirect(url_for('anghami'))


@app.route('/download_facebook', methods=['POST'])
def download_facebook():
    url = request.form.get('url')
    if not url:
        flash("يرجى إدخال رابط صحيح.", "error")
        return redirect(url_for('facebook'))

    try:
        unique_id = str(uuid.uuid4())[:8]
        output_template = os.path.join(DOWNLOAD_FOLDER, f'facebook_{unique_id}.%(ext)s')

        command = [
            'yt-dlp',
            '-o', output_template,
            url
        ]
        subprocess.run(command, check=True)

        for filename in os.listdir(DOWNLOAD_FOLDER):
            if unique_id in filename:
                full_path = os.path.join(DOWNLOAD_FOLDER, filename)
                return send_file(full_path, as_attachment=True)

        flash("حدث خطأ أثناء حفظ ملف فيسبوك.", "error")
        return redirect(url_for('facebook'))

    except subprocess.CalledProcessError as e:
        flash(f"خطأ أثناء التحميل من فيسبوك: {str(e)}", "error")
        return redirect(url_for('facebook'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

