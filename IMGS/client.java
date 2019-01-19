
package cloud.test;

import java.io.BufferedReader;

import java.io.ByteArrayOutputStream;

import java.io.DataOutputStream;

import java.io.File;

import java.io.FileInputStream;

import java.io.IOException;

import java.io.InputStreamReader;

import java.net.HttpURLConnection;

import java.net.URL;

import java.util.UUID;

/**

 * 图片上传

 * @author Cloud

 * @version 1.0

 */

public class UploadImage {

   private static final String MULTIPART_FORM_DATA="multipart/form-data";

   private static final String TWOHYPHENS = "--";

    private static final String BOUNDARY = "---------------------------"+UUID.randomUUID();

    private static final String LINEEND = "\r\n";

    private static final String FORMNAME="userfile";

    

    private String actionUrl;

    private int timeout;

    

    private String fileName;

    private byte[] data;

    private String imageType;

    

    /**

     * 初始化图片上传工具

     * @param actionUrl - 图片存储地址

     * @param timeout - 图片上传超时时间 （毫秒）

     */

    public UploadImage(String actionUrl,int timeout){

       this.actionUrl=actionUrl;

       this.timeout=timeout;

    }

    

    /**

     * 设置上传内容

     * @param fileName - 图片名称

     * @param data - 图片内容

     * @param imageType - 图片格式

     */

    public void setData(String fileName,byte[] data,ImageType imageType) throws Exception{

       this.fileName=fileName;

       this.data=data;

       this.imageType=imageType.getValue();

       

       if(imageType!=null){

          String extension =imageType.getValue().substring(imageType.getValue().indexOf("/")+1, imageType.getValue().length());

          this.fileName=fileName+"."+extension;

       }

    }

    

    /**

     * 上传

     * @return - 格式<br/>

     * {<br/>

     * &nbsp;&nbsp;&nbsp;&nbsp;"code": 200,<br/>

     * &nbsp;&nbsp;&nbsp;&nbsp;"msg": "upload success!",<br/>

     * &nbsp;&nbsp;&nbsp;&nbsp;"data": {<br/>

     * &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"t": "png",<br/>

     * &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"userpath": "01",<br/>

     * &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"md5": "6f8b47ec3b8ea08335cb6e13cbbe96dc",<br/>

     * &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"url": "01/6f8b47ec3b8ea08335cb6e13cbbe96dc.png"<br/>

     * &nbsp;&nbsp;&nbsp;&nbsp;}<br/>

     * }<br/>

     */

    public String upload(){

       return upload(null,null);

    }

    

    

    /**

     * 上传

     * @param actType - 图片处理命令

     * @param param - 图片处理参数

     * @return - 格式<br/>

     * {<br/>

     * &nbsp;&nbsp;&nbsp;&nbsp;"code": 200,<br/>

     * &nbsp;&nbsp;&nbsp;&nbsp;"msg": "upload success!",<br/>

     * &nbsp;&nbsp;&nbsp;&nbsp;"data": {<br/>

     * &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"t": "png",<br/>

     * &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"userpath": "01",<br/>

     * &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"md5": "6f8b47ec3b8ea08335cb6e13cbbe96dc",<br/>

     * &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"url": "01/6f8b47ec3b8ea08335cb6e13cbbe96dc.png"<br/>

     * &nbsp;&nbsp;&nbsp;&nbsp;}<br/>

     * }<br/>

     */

    public String upload(ActType actType,String param){

       HttpURLConnection conn = null;

        DataOutputStream output = null;

        BufferedReader input = null;

        

       try {

          URL url = new URL(actionUrl);

            conn = (HttpURLConnection) url.openConnection();

            conn.setConnectTimeout(timeout);

            conn.setDoInput(true);

            conn.setDoOutput(true);

            conn.setUseCaches(false);

            conn.setRequestMethod("POST");

            conn.setRequestProperty("Connection", "keep-alive");

            conn.setRequestProperty("Content-Type", MULTIPART_FORM_DATA + "; boundary=" + BOUNDARY);

            conn.connect();

            output = new DataOutputStream(conn.getOutputStream());

            

            StringBuilder sb = new StringBuilder();

            if(actType!=null&&param!=null){

             /**

               * 上传参数

               */

              sb.append(TWOHYPHENS + BOUNDARY + LINEEND);

              sb.append("Content-Disposition: form-data; name=\"act\"" + LINEEND);

              sb.append(LINEEND);

              sb.append(actType.getValue() + LINEEND);

              output.writeBytes(sb.toString());

              

              sb = new StringBuilder();

              sb.append(TWOHYPHENS + BOUNDARY + LINEEND);

              sb.append("Content-Disposition: form-data; name=\"param\"" + LINEEND);

              sb.append(LINEEND);

              sb.append(param + LINEEND);

              output.writeBytes(sb.toString());

            }

          

           /**

           * 上传图片

           */

          sb = new StringBuilder();

          sb.append(TWOHYPHENS + BOUNDARY + LINEEND);

          sb.append("Content-Disposition: form-data; name=\"" + FORMNAME + "\"; filename=\"" + fileName + "\"" + LINEEND);

          sb.append("Content-Type: " + imageType + LINEEND);

          sb.append(LINEEND);

           output.writeBytes(sb.toString());

           output.write(data, 0, data.length);

           output.writeBytes(LINEEND);

   

           /**

            * 上传结束

            */

           output.writeBytes(TWOHYPHENS + BOUNDARY + TWOHYPHENS + LINEEND);

           output.flush();

           

           /**

           * 返回信息

           */

           int code = conn.getResponseCode();

           System.out.println(code);

           if (code != 200) {

               throw new RuntimeException("请求'" + actionUrl + "'失败！");

           }

           input = new BufferedReader(new InputStreamReader(conn.getInputStream()));

           StringBuilder response = new StringBuilder();

           String oneLine;

           while ((oneLine = input.readLine()) != null) {

               response.append(oneLine + LINEEND);

           }

           return response.toString();

       } catch (IOException e) {

            throw new RuntimeException(e);

        } finally {

            try {

                if (output != null) {

                    output.close();

                }

                if (input != null) {

                    input.close();

                }

            } catch (IOException e) {

                throw new RuntimeException(e);

            }

            if (conn != null) {

                conn.disconnect();

            }

        }

    }

}
